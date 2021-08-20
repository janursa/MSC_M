from scipy.optimize import differential_evolution
import numpy as np
import json
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tellurium as te
import json
free_params = {
    'IL10_det':[10,100], # detrimental threshold for >48 exposure
    'maturity_t':[0,1], # early maturity threshold
    'early_diff_L':[0.05,0.45], # center of low membership function
    'early_diff_H':[0.55,0.95], # center of high membership function
    'late_diff_L':[0.05,0.45], # center of low membership function
    'late_diff_H':[0.55,0.95], # center of high membership function
    'a_early_diff_u':[1,100], # scale factor, upregulatory
    'a_early_diff_d':[1,100], # scale factor, downregulatory
    'a_late_diff_u':[1,100], # scale factor
    'a_late_diff_d':[1,100], # scale factor
    'diff_time':[15,45], # days required for full differentiation
    'ALP_maturity': [1,100], #correlation coeff between ALP and maturity
    'ARS_maturity': [1,100], #correlation coeff between ARS and maturity
    'a_Chen_2018': [0,100], #correlation coeff for the given study
    'a_Valles_2020_part1':[0,100] #correlation coeff for the given study
}
# load the samples from the original model
with open('observations.json') as json_file:
    observations = json.load(json_file)

def scale(x,factor_u, factor_d): 
    """
    Coorects the fuzzy controller's output 
    x: fuzzy output
    factor: scale factor
    """
    if x >= 0.5:
        f=2*(factor_u-1)*(x-0.5)+1
        return f
    else:
        f = (1/factor_d)*(2*(factor_d-1)*x+1)
        return f
class Fuzzy_IL10:
    def __init__(self,params,above_48h):
        self.antecedents = []
        self.consequents = []
        self.params = params
        #// define antecedents
        # the marks of IL10 memberships
        IL10_intervals_below_48h= [0,0.01,10,self.params['IL10_det'],100]
        IL10_intervals_above_48h= [0,0.01,0.1,10,100]
        if above_48h:
            IL10_intervals = IL10_intervals_above_48h
        else:
            IL10_intervals = IL10_intervals_below_48h
        IL10 = ctrl.Antecedent(np.arange(IL10_intervals[0], IL10_intervals[-1], .05), 'IL10')
        # print(IL10_intervals)
        IL10['Neg'] = fuzz.trimf(IL10.universe, [IL10_intervals[0], IL10_intervals[0],IL10_intervals[1]])
        IL10['Low'] = fuzz.trimf(IL10.universe, [IL10_intervals[0], IL10_intervals[1], IL10_intervals[2]])
        IL10['Stim'] = fuzz.trimf(IL10.universe, [IL10_intervals[1], IL10_intervals[2], IL10_intervals[3]])
        IL10['Det'] = fuzz.trapmf(IL10.universe, [IL10_intervals[2], IL10_intervals[3], IL10_intervals[-1], IL10_intervals[-1]])
        #// store
        self.antecedents.append(IL10)
#         IL10.view()
        #// define consequents
        range_value = np.arange(0, 1, .01)
        early_diff = ctrl.Consequent(range_value, 'early_diff')
        late_diff = ctrl.Consequent(range_value, 'late_diff')
        
        #// define membership functions
        sigma = .05
        diff_intervals = [0,self.params['early_diff_L'],.5,self.params['early_diff_H'], 1]
        early_diff['Z']=fuzz.gaussmf(range_value, diff_intervals[0], sigma)
        early_diff['L']=fuzz.gaussmf(range_value, diff_intervals[1], sigma)
        early_diff['M']=fuzz.gaussmf(range_value, diff_intervals[2], sigma)
        early_diff['H']=fuzz.gaussmf(range_value, diff_intervals[3], sigma)
        early_diff['VH']=fuzz.gaussmf(range_value, diff_intervals[4], sigma)

        diff_intervals = [0,self.params['late_diff_L'],.5,self.params['late_diff_H'], 1]
        late_diff['Z']=fuzz.gaussmf(range_value, diff_intervals[0], sigma)
        late_diff['L']=fuzz.gaussmf(range_value, diff_intervals[1], sigma)
        late_diff['M']=fuzz.gaussmf(range_value, diff_intervals[2], sigma)
        late_diff['H']=fuzz.gaussmf(range_value, diff_intervals[3], sigma)
        late_diff['VH']=fuzz.gaussmf(range_value, diff_intervals[4], sigma)
#         early_diff.view()

        #// Store
        self.consequents = [early_diff,late_diff]
        #// rules
        early_diff_rules = [
            ctrl.Rule(IL10['Stim'] , early_diff['VH']),
            ctrl.Rule(IL10['Low'] , early_diff['H']),
            ctrl.Rule(IL10['Neg'] , early_diff['M']),
            ctrl.Rule(IL10['Det'] , early_diff['L'])
        ]
        late_diff_rules = [
            ctrl.Rule(IL10['Stim'] , late_diff['VH']),
            ctrl.Rule(IL10['Low'] , late_diff['H']),
            ctrl.Rule(IL10['Neg'] , late_diff['M']),
            ctrl.Rule(IL10['Det'] , late_diff['L'])
        ]
        rules = early_diff_rules+late_diff_rules
        self.controler = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
        
    def forward(self,inputs):
        self.controler.input['IL10'] = inputs['IL10']
        self.controler.compute()
        # for item in self.consequents:
        #     item.view(sim=self.controler)
        outputs = self.controler.output
#         print(outputs)
        # outputs['early_diff'] = outputs['diff'] 
        # outputs['late_diff'] = outputs['diff'] 
        return outputs
def interactions(fs):
    return fs['f_IL10']

        
class Osteogenesis:
    def __init__(self,params):
        self.params = params
    def calculate_maturity(self,f_values,checkpoint):
        # print(f_values)
        k0 = 1/(self.params['diff_time']*24) # base diff rate 1/hour
        f_early = f_values['early_diff'] 
        f_late = f_values['late_diff'] 
        maturity_t = self.params['maturity_t']*self.params['diff_time']*24 # because given maturity_t in the parameters is between 0 and 1 1
        k_early = scale(f_early,factor_u = self.params['a_early_diff_u'], factor_d = self.params['a_early_diff_d'])*k0
        k_late = scale(f_late,factor_u = self.params['a_late_diff_u'], factor_d = self.params['a_late_diff_d'])*k0
        
        if checkpoint < maturity_t:
            maturity = k_early*checkpoint # no for loop
            return maturity
        else:
            maturity_0 = k_early*maturity_t
            maturity_1 = k_late*(checkpoint-maturity_t)
            return maturity_0+maturity_1
               

    def simulate(self,inputs,measurement_scheme,exposure_time): 
        """
        simulates one single run 
        """
        if exposure_time > 48: # fuzzy controller is defined differently based on the exposure time
            above_48h = True
        else:
            above_48h = False
            
        self.fuzzy_IL10 = Fuzzy_IL10(self.params,above_48h=above_48h)
        f_IL10 = self.fuzzy_IL10.forward(inputs)
        f_values = {'f_IL10':f_IL10}
        final_f_values = interactions(f_values)
        
        results= {}
        for target,checkpoint in measurement_scheme.items():
            checkpoint = checkpoint*24 #time in hours

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
            if study == 'Chen_2018' or study == 'Valles_2020_part1':
                results = self.simulate_osteogenesis_study(study)
            else:
                raise('Not defined')
            studies_results[study]= results
        return studies_results

    def simulate_osteogenesis_study(self,study):
        """
        Simulte one study
        """
        measurement_scheme = observations[study]['measurement_scheme']
        exposure_time = observations[study]['exposure_period']
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