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
from fuzzy_controllers import Fuzzy_IL10, Fuzzy_IL8,Fuzzy_TNFa,Fuzzy_Mg,Fuzzy_IL1b
all_params = {
    'ALP_M_n':1, # n in the equation ALP = a*(M^n + ALP_0)
    'ALP_0':.2, # the default value of ALP when maturity is zero
    'OC_0':.2, # the default value of OC when maturity is zero
    'ARS_0':.2, # the default value of ARS when maturity is zero
    'Mg_S':5, # stimulatory conc of Mg
    'Mg_D':30, # detrimental conc of Mg
    'IL10_d':50, # detrimental threshold for >48 exposure
    'IL1b_d':50, # detrimental threshold IL1b
    'IL8_M':25, # medium threshold for IL8
    'maturity_t':.5, # early maturity threshold
    'early_diff_L':.25, # center of low membership function
    'early_diff_H':.75, # center of high membership function
    'late_diff_L':.25, # center of low membership function
    'late_diff_H':.75, # center of high membership function
    'a_early_diff_u':2, # scale factor, upregulatory
    'a_early_diff_d':2, # scale factor, downregulatory
    'a_late_diff_u':2, # scale factor
    'a_late_diff_d':2, # scale factor
    'diff_time':30*24, # days required for full differentiation

    'a_Chen_2018_maturity_t':.5,
    'a_Chen_2018_ALP':2,
    'a_Chen_2018_ARS':2,

    'a_Valles_2020_IL10_maturity_t':.5, 
    'a_Valles_2020_IL10_ALP':2,
    'a_Valles_2020_IL10_ARS':2,
    
    'a_Valles_2020_TNFa_maturity_t':.5,
    'a_Valles_2020_TNFa_ALP':2,
    'a_Valles_2020_TNFa_ARS':2,

    'a_Qiao_2021_IL8_maturity_t':.5, 
    'a_Qiao_2021_IL8_ALP':2, 
    'a_Qiao_2021_IL1b_maturity_t':1, 
    'a_Qiao_2021_IL1b_ALP':2, 

    'a_Ber_2016_maturity_t':.5, # correction coeff of maturity threshold for the given study considering that cells are inherintly different
    'a_Ber_2016_ALP':.5, # correlation ALP to maturity
    'a_Ber_2016_OC':.5, 

    'a_Qiao_2021_Mg_maturity_t':.5,
    'a_Qiao_2021_Mg_ALP':10,
    'a_Qiao_2021_Mg_OC':.2,
}
free_params = {
    'ALP_M_n':[0,10], # n in the equation ALP = a*(M^n + ALP_0)
    'ALP_0':[0,1], # the default value of ALP when maturity is zero
    # 'OC_0':[0,1], # the default value of OC when maturity is zero
    # 'ARS_0':[0,1], # the default value of ARS when maturity is zero
    # 'Mg_S':[2,10], # stimulatory conc of Mg
    # 'Mg_D':[20,40], # detrimental conc of Mg
    # 'IL10_d':[10,100], # detrimental threshold for >48 exposure
    'IL1b_H':[10,100], # high threshold IL1b
    # 'IL8_M':[0,50], # medium threshold for IL8
    # 'maturity_t':[0,1], # early maturity threshold
    # 'early_diff_L':[0.05,0.45], # center of low membership function
    # 'early_diff_H':[0.55,0.95], # center of high membership function
    # 'late_diff_L':[0.05,0.45], # center of low membership function
    # 'late_diff_H':[0.55,0.95], # center of high membership function
    'a_early_diff_u':[1,100], # scale factor, upregulatory
    # 'a_early_diff_d':[1,100], # scale factor, downregulatory
    # 'a_late_diff_u':[1,100], # scale factor
    # 'a_late_diff_d':[1,100], # scale factor
    'diff_time':[15*24,45*24], # days required for full differentiation

    # 'a_Chen_2018_maturity_t':[0,1],
    # 'a_Chen_2018_ALP':[0,10],
    # 'a_Chen_2018_ARS':[0,10],

    # 'a_Valles_2020_IL10_maturity_t':[0,1], 
    # 'a_Valles_2020_IL10_ALP':[0,1000],
    # 'a_Valles_2020_IL10_ARS':[0,1000],
    
    # 'a_Valles_2020_TNFa_maturity_t':[0,1],
    # 'a_Valles_2020_TNFa_ALP':[0,1000],
    # 'a_Valles_2020_TNFa_ARS':[0,1000],

    # 'a_Qiao_2021_IL8_maturity_t':[0,1], 
    # 'a_Qiao_2021_IL8_ALP':[0,200], 
    # 'a_Qiao_2021_IL1b_maturity_t':[0,1], 
    'a_Qiao_2021_IL1b_ALP':[0,200], 

    # 'a_Ber_2016_maturity_t':[0,1], # correction coeff of maturity threshold for the given study considering that cells are inherintly different
    # 'a_Ber_2016_ALP':[0,1], # correlation ALP to maturity
    # 'a_Ber_2016_OC':[0,1], 

    # 'a_Qiao_2021_Mg_maturity_t':[0,1],
    # 'a_Qiao_2021_Mg_ALP':[0,50],
    # 'a_Qiao_2021_Mg_OC':[0,1],
}

class Osteogenesis:
    def __init__(self,params,debug=False):
        self.debug = debug
        self.params = params
        self.controlers = {'IL10_above_48h':Fuzzy_IL10(self.params,above_48h=True),
                            'IL10_below_48h':Fuzzy_IL10(self.params,above_48h=False),
                            'IL8':Fuzzy_IL8(self.params),
                            'IL1b':Fuzzy_IL1b(self.params),
                            'TNFa':Fuzzy_TNFa(self.params),
                            'Mg':Fuzzy_Mg(self.params)}
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
        # if x >= 0.5:
        #     f=(factor_u-1)*(x-0.5)*2+1
        #     return f
        # else:
        #     f = (1/factor_d)*(1-2*(1-factor_d)*x)
        #     return f
        if x >= 0.5:
            factor = factor_u
        else:
            factor = factor_d
        f=(factor-1)*abs(x-0.5)*2+1
        if x >= 0.5:
            return f
        else:
            return 1/f
    @staticmethod
    def adjust_maturity_t(study,maturity_t):
        """
        correct maturity threshold bsed on each study
        """
        
        return maturity_t*correction_coeff

    def calculate_maturation(self,study,f_values,checkpoint,target):
        
        k0 = 1/(self.params['diff_time']) # base diff rate 1/hour
        #// k_early and k_late are the corrected maturation rate
        if 'early_diff' in f_values:
            f_early = f_values['early_diff'] # fuzzy output for early maturation
            k_early = 2*k0 * self.scale(x = f_early,factor_u = self.params['a_early_diff_u'], factor_d = self.params['a_early_diff_d']) # 2 is because the normal f value is 0.5
        else:
            k_early = k0
        if 'late_diff' in f_values:
            f_late = f_values['late_diff'] 
            k_late = 2*k0 * self.scale(x = f_late,factor_u = self.params['a_late_diff_u'], factor_d = self.params['a_late_diff_d'])
        else:
            k_late = k0
        #// calculate maturity related parameters
        maturity_t_correction_factor = self.params['a_'+study+'_maturity_t'] # to correct maturity threshold for each experiment considering that cells are inherintly differenmt
        adjusted_maturity_t = maturity_t_correction_factor * self.params['maturity_t']
        maturity_t_scalled = adjusted_maturity_t*self.params['diff_time'] # because given maturity_t in the parameters is between 0 and 1 1
        
        def calculate_maturity(checkpoint,maturity_t_h,k_early = None,k_late = None):
            if checkpoint < maturity_t_h: # if the given time is below the threshold
                maturity = checkpoint*k_early
            else:
                maturity = maturity_t_h*k_early + (checkpoint-maturity_t_h)*k_late

            if maturity > 1: # should be between 0 and 1
                maturity = 1
            return maturity

        #// calculate ALP, OC, and ARS based on maturity
        maturity = calculate_maturity(checkpoint = checkpoint,maturity_t_h=maturity_t_scalled,
                k_early=k_early,k_late=k_late)
        # print('checkpoint {} fs {} maturity {}'.format(checkpoint,f_values, maturity))

        if target == 'ALP':
            ALP_M_coeff = self.params['a_'+study+'_ALP']
            if maturity < adjusted_maturity_t:
                ALP = (maturity**self.params['ALP_M_n'] + self.params['ALP_0']) * ALP_M_coeff
            else:
                ALP =(adjusted_maturity_t + self.params['ALP_0']) * ALP_M_coeff
            if self.debug:
                print('checkpoint {}, fs {}, maturity {}, maturity_t {}, ALP {}'.format(checkpoint,f_values, round(maturity,4),round(adjusted_maturity_t,4),round(ALP,4)))

            return ALP
        elif target == 'ARS':
            ARS_M_coeff = self.params['a_'+study+'_ARS']
            ARS = (maturity + self.params['ARS_0']) * ARS_M_coeff
            return ARS
        elif target == 'OC':
            OC_M_coeff = self.params['a_'+study+'_OC']
            OC = (maturity + self.params['OC_0']) * OC_M_coeff
            return OC
        else:
            raise('invlid input')



    def simulate(self,study,inputs,measurement_scheme,exposure_time): 
        """
        simulates one single run 
        """
        if exposure_time > 48: # fuzzy controller is defined differently based on the exposure time
            IL10_controler = self.controlers['IL10_above_48h']
        else:
            IL10_controler = self.controlers['IL10_below_48h']
        IL8_controller = self.controlers['IL8']
        IL1b_controller = self.controlers['IL1b']
        TNFa_controller = self.controlers['TNFa']
        Mg_controller = self.controlers['Mg']

        fs = {'IL10':None,'IL8':None,'IL1b':None, 'TNFa':None, 'Mg':None}
        if 'IL10' in inputs.keys():
            f_IL10 = IL10_controler.forward({'IL10':inputs['IL10']})
            fs['IL10'] = f_IL10
        if 'IL8' in inputs.keys():
            f_IL8 = IL8_controller.forward({'IL8':inputs['IL8']})
            fs['IL8'] = f_IL8
        if 'IL1b' in inputs.keys():
            f_IL1b = IL1b_controller.forward({'IL1b':inputs['IL1b']})
            fs['IL1b'] = f_IL1b
        if 'TNFa' in inputs.keys():
            f_TNFa = TNFa_controller.forward({'TNFa':inputs['TNFa']})
            fs['TNFa'] = f_TNFa
        if 'Mg' in inputs.keys():
            ff = Mg_controller.forward({'Mg':inputs['Mg']})
            fs['Mg'] = ff

        final_f_values = self.interactions(fs)
        results= {}

        for target,checkpoints in measurement_scheme.items():
            results[target] = []
            for checkpoint in checkpoints:
                result=  self.calculate_maturation(study = study, f_values=final_f_values,
                                                checkpoint = checkpoint,target=target)
                results[target].append(result)

        return results

class MSC_model:
    def __init__(self,free_params,debug=False):
        self.debug=debug
        for key,value in free_params.items():
            all_params[key] = value
        self.params = all_params
        self.osteogenesis = Osteogenesis(self.params,debug=self.debug)
        # TODO: another model should be created for inflammatory reponse
    def simulate_studies(self):
        """
        Simulate all studies
        """
        studies_results = {}
        for study in observations['studies']:
            results = self.simulate_osteogenesis_study(study)
            
            studies_results[study]= results
        return studies_results

    def simulate_osteogenesis_study(self,study):
        """
        Simulte one study
        """
        measurement_scheme = observations[study]['measurement_scheme']
        exposure_time = observations[study]['exposure_time']
        IDs = observations[study]['IDs']
        results = {}
        for ID in IDs:
            inputs = observations[study][ID]['inputs']
            if self.debug:
                print('\n',ID)
            ID_results = self.osteogenesis.simulate(study=study,inputs=inputs,measurement_scheme=measurement_scheme,exposure_time=exposure_time)
            
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
                abs_diff =abs(np.array(ID_results[target])-np.array(ID_observations[target]['mean']))
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
    
    obj = MSC_model(free_params={})
    print('\n',obj.run())