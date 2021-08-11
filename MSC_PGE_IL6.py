import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tellurium as te
# %config Completer.use_jedi = False
# showOriginalModelString = True
#TODO: watch out that ctrl gets reset at each calibration run
# free_params = {
#     'TNFa_l': 5
# }

class Fuzzy_MSC:
    def __init__(self,params):
        self.antecedents = []
        self.consequents = []
        self.params = params
        TNFa_0 = self.params['TNFa'][0]; TNFa_1 = self.params['TNFa'][1]; TNFa_end = self.params['TNFa'][2] 
        IL10_0 = self.params['IL10'][0]; IL10_end = self.params['IL10'][-1]; 
        #// define antecedents
        TNFa = ctrl.Antecedent(np.arange(TNFa_0, TNFa_end, .05), 'TNFa')
        IL10 = ctrl.Antecedent(np.arange(IL10_0, IL10_end, .05), 'IL10')
        #// define memberships
        TNFa['L'] = fuzz.trimf(TNFa.universe, [TNFa_0, TNFa_0, TNFa_1])
        TNFa['M'] = fuzz.trimf(TNFa.universe, [TNFa_0, TNFa_1, TNFa_end])
        TNFa['H'] = fuzz.trimf(TNFa.universe, [TNFa_1, TNFa_end, TNFa_end])

        IL10['L'] = fuzz.trimf(IL10.universe, [IL10_0, IL10_0, IL10_end])
        IL10['H'] = fuzz.trimf(IL10.universe, [IL10_0, IL10_end, IL10_end])
        #// store
        self.antecedents.append(TNFa)
        self.antecedents.append(IL10)
#         IL10.view()
#         TNFa.view()
        
        #// define consequents
        range_value = np.arange(0, 1, .01)
        IL6 = ctrl.Consequent(range_value, 'IL6')
        PGE2 = ctrl.Consequent(range_value, 'PGE2')
        
        #// define membership functions
        sigma = .05
        intervals = [0,.5, 1]
        IL6['L']=fuzz.gaussmf(range_value, intervals[0], sigma)
        IL6['M']=fuzz.gaussmf(range_value, intervals[1], sigma)
        IL6['H']=fuzz.gaussmf(range_value, intervals[2], sigma)
#         IL6.automf(3)
        intervals = [0,.25,.5,.75, 1]
        PGE2['VL']=fuzz.gaussmf(range_value, intervals[0], sigma)
        PGE2['L']=fuzz.gaussmf(range_value, intervals[1], sigma)
        PGE2['M']=fuzz.gaussmf(range_value, intervals[2], sigma)
        PGE2['H']=fuzz.gaussmf(range_value, intervals[3], sigma)
        PGE2['VH']=fuzz.gaussmf(range_value, intervals[4], sigma)
#         PGE2.automf(5)
        
        #// Store
        self.consequents = [IL6,PGE2]
        #// rules
        TNF_rules = [
        ctrl.Rule(TNFa['L'] , IL6['L']),
        ctrl.Rule(TNFa['M'] , IL6['M']),
        ctrl.Rule(TNFa['H'] , IL6['H'])
        ]
        
        PGE2_rules = [
        ctrl.Rule( TNFa['L'] , PGE2['VL']),
        ctrl.Rule( TNFa['M'] & IL10['L'] , PGE2['L']),
        ctrl.Rule( TNFa['M'] & IL10['H'] , PGE2['M']),
        ctrl.Rule( TNFa['H'] & IL10['L'] , PGE2['H']),
        ctrl.Rule( TNFa['H'] & IL10['H'] , PGE2['VH'])
        ]
        
        rules = TNF_rules + PGE2_rules
        self.controler = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
        
    def forward(self,inputs):
        for key,value in inputs.items():
            self.controler.input[key] = value
        self.controler.compute()
        # for item in self.consequents:
        #     item.view(sim=self.controler)
        outputs = self.controler.output
        # outputs['IL6'] *= (self.params['IL6'][-1]-self.params['IL6'][0])+self.params['IL6'][0]
        # outputs['PGE2'] *= (self.params['PGE2'][-1]-self.params['PGE2'][0])+self.params['PGE2'][0]
        return outputs
        

        
class MSC_model:
    def __init__(self,free_params_keys,free_params_values,setup_info):
        self.setup_info = setup_info
        #// assmeble the key and values for the free params
        free_params = {}
        for key,value in  zip(free_params_keys,free_params_values):
            free_params[key] = value

        self.params = {
            'TNFa': [0,free_params['TNF_a_l'],10],
            'IL10': [0,1]
        }
        self.params = {**self.params, **free_params}
        self.data = {'IL6':[0],'PGE2':[0]}
        self.fuzzy_model = Fuzzy_MSC(self.params)
        self.ODE_model = te.loada("""
            IL6 = 0;
            IL6_prod = 1;
            K_IL6_prod = 100;
            K_IL6_sat = 100;
            $IL6_prod -> IL6; K_IL6_prod - K_IL6_sat*IL6;
            
            PGE2 = 0;
            PGE2_prod = 1;
            K_PGE2_prod = 100;
            K_PGE2_sat = 100;
            $PGE2_prod -> PGE2; K_PGE2_prod - K_PGE2_sat*PGE2;

            maturity_prod = 1;
            maturity = 0;
            $maturity_prod->maturity; .1;

            
        """)
    def run(self):
        #// get the coeff from fuzzy model
        fuzzy_results = self.fuzzy_model.forward(self.setup_info['inputs'])
        f_IL6 = fuzzy_results['IL6']
        f_PGE2 = fuzzy_results['PGE2']
        #// update the ODE model based on fuzzy coeff
        self.ODE_model['K_IL6_prod'] = self.params['K_IL6_prod_0']*(1+self.params['K_IL6_prod_beta']*f_IL6)
        self.ODE_model['K_PGE2_prod'] = self.params['K_PGE2_prod_0']*(1+self.params['K_PGE2_prod_beta']*f_PGE2)

        self.ODE_model['K_IL6_sat'] = self.params['K_IL6_sat']
        self.ODE_model['K_PGE2_sat'] = self.params['K_PGE2_sat']
        #// run the ODE model
        selections = ['TIME','IL6','PGE2']
        results = self.ODE_model.simulate(0,self.setup_info['duration'],self.setup_info['duration'],selections= selections)
        # self.ODE_model.plot()
        return {'IL6':results['IL6'][-1],'PGE2':results['PGE2'][-1]}




        
        