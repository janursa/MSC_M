from scipy.optimize import differential_evolution
import numpy as np
import json
import sys
import os
import pathlib
current_file = pathlib.Path(__file__).parent.absolute()

# import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json
from observations import observations
# from fuzzy_controllers import *
# from pympler import muppy,tracker
dir_to_binds = os.path.join(current_file,'fuzzy_cpp/build/binds')
sys.path.insert(0,dir_to_binds)
from fuzzy_cpp import *
import parameters 

class Osteogenesis:
    def __init__(self,params,debug=False):
        self.debug = debug
        self.params = params
        self.controlers = {
                            'IL10_above_48h':Fuzzy_IL10(self.params, True),
                            'IL10_below_48h':Fuzzy_IL10(self.params, False),
                            'IL8_IL1b':Fuzzy_IL8_IL1b(self.params),
                            'TNFa':Fuzzy_TNFa(self.params),
                            'Mg':Fuzzy_Mg(self.params)
                            }



    def interactions(self,fs):
        """
        defines the interaction between different fuzzy values
        """

        for key,value in fs.items():
            if value != None:
                return value

    def scale(self,x,factor_stim,factor_inhib):
        """
        Scale the fuzzy controller's output cosidering that the origin is x=0.5
        The scalling is done differently for x > 0.5 than x < 0.5
        x: fuzzy output
        factor: scale factor
        """
        if x >=0.5:
            f = 2*factor_stim*(x-0.5)+1
        else:
            f = 2*factor_inhib*(x-0.5)+1
            # print(x,factor_inhib,f)


        if f <=0:
            f = 0
        return f
        # if x >= 0.5:
        #     return 2*factor_u*abs(x-0.5)+1
        # else:
        #     factor = factor_d
        # f=(factor-1)*abs(x-0.5)*2+1
        # if x >= 0.5:
        #     return f
        # else:
        #     return 1/f
    @staticmethod
    def adjust_maturity_t(study,maturity_t):
        """
        correct maturity threshold bsed on each study
        """

        return maturity_t*correction_coeff
    @staticmethod
    def determine_correction_factor(study,params,f_type='maturity_t'):
        """
        To correct maturity threshold for each experiment considering that cells
        are inherintly differenmt

        """

        if (study == 'Qiao_2021_IL8_IL1b' or study == 'Qiao_2021_IL8' or study == 'Qiao_2021_IL1b'or study == 'Qiao_2021_Mg'):
            study = 'Qiao_2021'

        if (study == 'Valles_2020_TNFa' or study == 'Valles_2020_IL10' ):
            study = 'Valles_2020'

        prefix = 'a_'+study
        tag = prefix+'_'+f_type
        return params[tag]
    def calculate_maturation(self,study,f_values,checkpoint,target):

        k0 = 1/(self.params['diff_time']) # base diff rate 1/hour
        #// k_early and k_late are the corrected maturation rate
        if 'early_diff' in f_values:
            f_early = f_values['early_diff'] # fuzzy output for early maturation
            k_early = k0 * self.scale(x = f_early,factor_stim= self.params['a_early_diff_stim'],factor_inhib= self.params['a_early_diff_inhib'])
        else:
            k_early = k0
        if 'late_diff' in f_values:
            f_late = f_values['late_diff']
            k_late = k0 * self.scale(x = f_late,factor_stim = self.params['a_late_diff_stim'],factor_inhib = self.params['a_late_diff_inhib'])
            # print('k_late ',k_late)
        else:
            k_late = k0
        #// calculate maturity related parameters
        # maturity_t_correction_factor = self.determine_correction_factor(study = study, params = self.params, f_type='maturity_t') # to correct maturity threshold for each experiment considering that cells are inherintly differenmt
        # adjusted_maturity_t = maturity_t_correction_factor * self.params['maturity_t']
        adjusted_maturity_t = self.params['maturity_t']
        maturity_t_scalled = adjusted_maturity_t*self.params['diff_time'] # because given maturity_t in the parameters is between 0 and 1 1

        def calculate_maturity(checkpoint,maturity_t_h,k_early = None,k_late = None):
            if checkpoint < maturity_t_h: # if the given time is below the threshold
                maturity = checkpoint*k_early
                # if study == 'Valles_2020_IL10':
                #     print(maturity)
            else:
                maturity = maturity_t_h*k_early + (checkpoint-maturity_t_h)*k_late
            # print('maturity ',maturity)
            if maturity > 1: # should be between 0 and 1
                maturity = 1
            return maturity

        #// calculate ALP, OC, and ARS based on maturity
        maturity = calculate_maturity(checkpoint = checkpoint,maturity_t_h=maturity_t_scalled,
                k_early=k_early,k_late=k_late)
        # if self.debug:
        #     print('checkpoint {} fs {} maturity {}'.format(checkpoint,f_values, round(maturity,3)))

        if target == 'ALP':
            ALP_M_coeff = self.determine_correction_factor(study = study, params = self.params, f_type='ALP')
            if maturity < adjusted_maturity_t:
                ALP = (maturity + self.params['ALP_0'])**self.params['ALP_M_n'] * ALP_M_coeff
            else:
                ALP =(adjusted_maturity_t + self.params['ALP_0'])**self.params['ALP_M_n'] * ALP_M_coeff
            # if self.debug:
            #     print('checkpoint {}, fs {}, maturity {}, maturity_t {}, ALP {}'.format(checkpoint,f_values, round(maturity,4),round(adjusted_maturity_t,4),round(ALP,4)))
            # if study == 'Valles_2020_IL10':
            #     print('fs {}, maturity {}, maturity_t {}, maturity_t_scalled {} checkpoint {}'.format(round(f_values['early_diff'],3), round(maturity,3),round(adjusted_maturity_t,4),maturity_t_scalled,checkpoint))

            return ALP
        elif target == 'ARS':
            ARS_M_coeff = self.determine_correction_factor(study = study, params = self.params, f_type='ARS')
            ARS = (maturity + self.params['ARS_0'])**self.params['ARS_M_n'] * ARS_M_coeff
            if self.debug:
                print('checkpoint {}, fs {}, maturity {}, maturity_t {}, ARS {}'.format(checkpoint,f_values, round(maturity,4),round(adjusted_maturity_t,4),round(ARS,4)))

            return ARS
        elif target == 'OC':
            OC_M_coeff = self.determine_correction_factor(study = study, params = self.params, f_type='OC')
            OC = (maturity + self.params['OC_0'])**self.params['OC_M_n'] * OC_M_coeff
            if self.debug:
                print('checkpoint {}, fs {}, maturity {}, maturity_t {}, OC {}'.format(checkpoint,f_values, round(maturity,4),round(adjusted_maturity_t,4),round(OC,4)))
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
        IL8_IL1b_controller = self.controlers['IL8_IL1b']
        TNFa_controller = self.controlers['TNFa']
        Mg_controller = self.controlers['Mg']

        fs = {'IL10':None,'IL8':None,'IL1b':None, 'TNFa':None, 'Mg':None}

        IL8_flag = 'IL8' in inputs.keys()
        IL1b_flag = 'IL1b' in inputs.keys()
        IL10_flag = 'IL10' in inputs.keys()
        TNFa_flag = 'TNFa' in inputs.keys()
        Mg_flag = 'Mg' in inputs.keys()


        if IL10_flag:
            IL10_controler.reset()
            f_IL10 = IL10_controler.forward({'IL10':inputs['IL10']})
            fs['IL10'] = f_IL10

        if IL8_flag or IL1b_flag:
            IL8_IL1b_controller.reset()
            ff = IL8_IL1b_controller.forward(inputs)
            fs['IL8_IL1b'] = ff
        if TNFa_flag:
            TNFa_controller.reset()
            f_TNFa = TNFa_controller.forward({'TNFa':inputs['TNFa']})
            fs['TNFa'] = f_TNFa
        if Mg_flag:
            Mg_controller.reset()
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
    def __init__(self,free_params,fixed_params,observations, debug=False):
        self.debug=debug
        for key,value in free_params.items():
            fixed_params[key] = value
        self.params = fixed_params
        self.observations = observations
        self.osteogenesis = Osteogenesis(self.params,debug=self.debug)
        # TODO: another model should be created for inflammatory reponse
    def simulate_studies(self):
        """
        Simulate all studies
        """
        studies_results = {}
        for study in self.observations['studies']:
            results = self.simulate_osteogenesis_study(study)

            studies_results[study]= results
        return studies_results

    def simulate_osteogenesis_study(self,study):
        """
        Simulte one study
        """
        if self.debug:
            print('\n **** ', study,'*** \n')
        measurement_scheme = self.observations[study]['measurement_scheme']
        exposure_time = self.observations[study]['exposure_time']
        IDs = self.observations[study]['IDs']
        results = {}
        for ID in IDs:
            inputs = self.observations[study][ID]['inputs']
            if self.debug:
                print('\n',ID)
                # print('inputs:',inputs)
            ID_results = self.osteogenesis.simulate(study=study,inputs=inputs,measurement_scheme=measurement_scheme,exposure_time=exposure_time)
            results[ID] = ID_results

        return results
    def cost_study(self,study,study_results):
        """
        calculates cost values for each ID of the given study
        """
        measurement_scheme = self.observations[study]['measurement_scheme']
        errors = {}
        for ID, ID_results in study_results.items():
            ID_observations = self.observations[study][ID]['expectations']
            target_errors = {}
            for target in measurement_scheme.keys():
                abs_diff =abs(np.array(ID_results[target])-np.array(ID_observations[target]['mean']))
                means = [ID_observations[target]['mean'],ID_results[target]]
                mean = np.mean(means)
                target_error = abs_diff/mean
                target_errors[target] = target_error
            errors[ID] = target_errors
        return errors
    def cost_studies(self,studies_results):
        """
        Calculates cost values for all studies
        """
        errors = {}
        for study,study_results in studies_results.items():
            errors[study] = self.cost_study(study,study_results)
        return errors
    def cost_individual_measurements(self,studies_results):
        """
        Calculates overall costs by averaging on each measuremnt item/day
        """
        costs = []
        for study,study_results in studies_results.items():
            for ID, ID_results in study_results.items():
                for target,target_results in ID_results.items():
                    for i in range(len(target_results)):
                        sim = target_results[i]
                        exp = self.observations[study][ID]['expectations'][target]['mean'][i]
                        mean = (sim+exp)/2
                        diff = abs(sim-exp)
                        error = diff/mean
                        costs.append(error)
        return np.mean(costs)

    def run(self):
        results = self.simulate_studies()
        error = self.cost_individual_measurements(results)
        return error
def single_run(free_params,fixed_params,observations):
    obj = MSC_model(fixed_params = fixed_params,free_params=free_params,observations=observations)
    error = obj.run()
    return error
if __name__ == '__main__':
    # tr = tracker.SummaryTracker()
    # for i in range(100000):
    obs,free_params = parameters.specification('all')
    error = single_run(free_params=free_params, fixed_params=parameters.fixed_params,observations=obs)
        # if i%500==0:
        #     print('Iteration ',i)
        #     tr.print_diff()
