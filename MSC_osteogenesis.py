from scipy.optimize import differential_evolution
import numpy as np
import json
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tellurium as te
import json
from observations import observations
from fuzzy_controllers import Fuzzy_IL10, Fuzzy_IL8
free_params = {
    'IL10_det':[10,100], # detrimental threshold for >48 exposure
    'IL8_M':[0,50], # medium threshold for IL8
    'maturity_t':[0,1], # early maturity threshold
    'early_diff_L':[0.05,0.45], # center of low membership function
    'early_diff_H':[0.55,0.95], # center of high membership function
    'late_diff_L':[0.05,0.45], # center of low membership function
    'late_diff_H':[0.55,0.95], # center of high membership function
    'a_early_diff_u':[1,100], # scale factor, upregulatory
    'a_early_diff_d':[1,100], # scale factor, downregulatory
    'a_late_diff_u':[1,100], # scale factor
    'a_late_diff_d':[1,100], # scale factor
    'diff_time':[15*24,45*24], # days required for full differentiation
    'ALP_maturity': [1,100], #correlation coeff between ALP and maturity
    'ARS_maturity': [1,100], #correlation coeff between ARS and maturity
    'a_Chen_2018': [0,100], #correlation coeff for the given study
    'a_Valles_2020_IL10':[0,100], #correlation coeff for the given study
    'a_Valles_2020_TNFa':[0,100], #correlation coeff for the given study
    'a_Qiao_2021':[0,100] #correlation coeff for the given study
}

class Osteogenesis:
    def __init__(self,params):
        self.params = params
        self.controlers = {'IL10_above_48h':Fuzzy_IL10(self.params,above_48h=True),
                            'IL10_below_48h':Fuzzy_IL10(self.params,above_48h=False),
                            'IL8':Fuzzy_IL8(self.params)}
    def interactions(self,fs):
        """
        defines the interaction between different fuzzy values
        """
        for key,value in fs.items():
            if value != None:
                return value

    def scale(self,x,factor_u, factor_d): 
        """
        Scale the fuzzy controller's output cosidering that the origin is x=0.5
        The scalling is done differently for x > 0.5 than x < 0.5
        x: fuzzy output
        factor: scale factor
        """
        if x >= 0.5:
            f=2*(factor_u-1)*(x-0.5)+1
            return f
        else:
            f = (1/factor_d)*(2*(factor_d-1)*x+1)
            return f
    def calculate_maturity(self,f_values,checkpoint):
        
        k0 = 1/(self.params['diff_time']) # base diff rate 1/hour
        # print(f_values)
        f_early = f_values['early_diff'] 
        f_late = f_values['late_diff'] 

        k_early = k0*self.scale(f_early,factor_u = self.params['a_early_diff_u'], factor_d = self.params['a_early_diff_d'])
        k_late = k0*self.scale(f_late,factor_u = self.params['a_late_diff_u'], factor_d = self.params['a_late_diff_d'])
        
        maturity_t = self.params['maturity_t']*self.params['diff_time'] # because given maturity_t in the parameters is between 0 and 1 1

        if checkpoint < maturity_t:
            maturity = k_early*checkpoint # no for loop
            return maturity
        else:
            # maturity_0 = k_early*maturity_t
            # maturity_1 = k_late*(checkpoint-maturity_t)
            # return maturity_0+maturity_1
            maturity = k_late*(checkpoint)
            return maturity
    def simulate(self,inputs,measurement_scheme,exposure_time): 
        """
        simulates one single run 
        """
        if exposure_time > 48: # fuzzy controller is defined differently based on the exposure time
            IL10_controler = self.controlers['IL10_above_48h']
        else:
            IL10_controler = self.controlers['IL10_below_48h']
        IL8_controller = self.controlers['IL8']

        fs = {'IL10':None,'IL8':None}
        if 'IL10' in inputs.keys():
            f_IL10 = IL10_controler.forward({'IL10':inputs['IL10']})
            fs['IL10'] = f_IL10
        if 'IL8' in inputs.keys():
            f_IL8 = IL8_controller.forward({'IL8':inputs['IL8']})
            fs['IL8'] = f_IL8

        final_f_values = self.interactions(fs)
        results= {}
        for target,checkpoint in measurement_scheme.items():
            checkpoint = checkpoint #time in hours

            maturity =  self.calculate_maturity(f_values=final_f_values,
                                                checkpoint = checkpoint)
            if target == 'ALP':
                correction = self.params['ALP_maturity']
            elif target == 'ARS':
                correction = self.params['ARS_maturity']
            results[target] = maturity*correction


        return results

class MSC_model:
    def __init__(self,params):
        self.params = params
        self.osteogenesis = Osteogenesis(params)
        # TODO: another model should be created for inflammatory reponse
    def simulate_studies(self):
        """
        Simulate all studies
        """
        studies_results = {}
        for study in observations['studies']:
            if study == 'Chen_2018' or study == 'Valles_2020_part1' or study == 'Qiao_2021':
                results = self.simulate_osteogenesis_study(study)
            else:
                raise('Not defined')
            studies_results[study]= results
        return studies_results

    def simulate_osteogenesis_study(self,study):
        """
        Simulte one study
        """
        # print('Simulates osteogenesis for study {}'.format(study))
        measurement_scheme = observations[study]['measurement_scheme']
        exposure_time = observations[study]['exposure_time']
        IDs = observations[study]['IDs']
        correction_factor = self.params['a_'+study]
        results = {}
        for ID in IDs:
            inputs = observations[study][ID]['inputs']
            ID_results = self.osteogenesis.simulate(inputs,measurement_scheme,exposure_time=exposure_time)
            #// correct the results
            for target,value in ID_results.items():
                ID_results[target] = value*correction_factor
            results[ID] = ID_results
                
        return results
    def cost_study(self,study,study_results):
        """
        calculates cost values for each ID of the given study
        """
        measurement_scheme = observations[study]['measurement_scheme']
        errors = {}
        for ID, ID_results in study_results.items():
            ID_observations = observations[study][ID]['expectations']
            tag_errors = []
            for target in measurement_scheme.keys():
                abs_diff =abs(ID_results[target]-ID_observations[target]['mean'])
                means = [ID_observations[target]['mean'],ID_results[target]]
                mean = np.mean(means)
                tag_error = abs_diff/mean
                tag_errors.append(tag_error)
            errors[ID] = np.mean(tag_errors)
        return errors
    def cost_studies(self,studies_results):
        """
        Calculates cost values for all studies
        """
        errors = {}
        for study,study_results in studies_results.items():
            errors[study] = self.cost_study(study,study_results)
        return errors
    def run(self):
        results = self.simulate_studies()
        errors = self.cost_studies(results)
        error = np.mean([np.mean(list(study_errors.values())) for study_errors in errors.values()])
        return error
if __name__ == '__main__':
    params = {}
    for key,value in free_params.items():
        params[key] = np.mean(value)
    obj = MSC_model(params)
    print(obj.run())