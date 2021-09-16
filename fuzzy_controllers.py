import numpy as np
import json
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
class Fuzzy_controller:
    def __init__(self,params):
        self.antecedents = {}
        self.consequents = {}
        self.params = params
        self.default_inputs = {}
    def define_antecedents(self):
        pass
    def define_consequents(self):
        #// define consequents
        range_value = np.arange(0, 1, .01)
        early_diff = ctrl.Consequent(range_value, 'early_diff')
        late_diff = ctrl.Consequent(range_value, 'late_diff')
        
        #// define membership functions
        sigma = .05
        diff_intervals = [0,self.params['early_diff_L'],.5,self.params['early_diff_H'],self.params['early_diff_VH'], 1]
        early_diff['Z']=fuzz.gaussmf(range_value, diff_intervals[0], sigma)
        early_diff['L']=fuzz.gaussmf(range_value, diff_intervals[1], sigma)
        early_diff['M']=fuzz.gaussmf(range_value, diff_intervals[2], sigma)
        early_diff['H']=fuzz.gaussmf(range_value, diff_intervals[3], sigma)
        early_diff['VH']=fuzz.gaussmf(range_value, diff_intervals[4], sigma)
        early_diff['EH']=fuzz.gaussmf(range_value, diff_intervals[5], sigma)


        diff_intervals = [0,self.params['late_diff_L'],.5,self.params['late_diff_H'], 1]
        late_diff['Z']=fuzz.gaussmf(range_value, diff_intervals[0], sigma)
        late_diff['L']=fuzz.gaussmf(range_value, diff_intervals[1], sigma)
        late_diff['M']=fuzz.gaussmf(range_value, diff_intervals[2], sigma)
        late_diff['H']=fuzz.gaussmf(range_value, diff_intervals[3], sigma)
        late_diff['VH']=fuzz.gaussmf(range_value, diff_intervals[4], sigma)
#         early_diff.view()
        #// Store
        self.consequents['early_diff'] = early_diff
        self.consequents['late_diff'] = late_diff
    def define_rules(self):
        pass
    def forward(self,inputs):
        # print('default_inputs: {}'.format(self.default_inputs))
        for key,value in inputs.items():
            self.default_inputs[key] = value
        # print('real inputs: {}'.format(self.default_inputs))
        for key,value in self.default_inputs.items():
            self.controler.input[key] = value
        self.controler.compute()
        # for key,item in self.consequents.items():
        #     item.view(sim=self.controler)
        outputs = self.controler.output
        # print('outputs: {}'.format(outputs))
        return outputs
class Fuzzy_IL10(Fuzzy_controller):
    def __init__(self,params,above_48h):
        super().__init__(params)
        self.define_antecedents(above_48h)
        self.define_consequents()
        self.define_rules()
    def define_antecedents(self,above_48h):
        #// define antecedents
        # the marks of IL10 memberships
        IL10_intervals_below_48h= [0,0.01,10,self.params['IL10_d'],100]
        IL10_intervals_above_48h= [0,0.01,0.1,10,100]
        if above_48h:
            IL10_intervals = IL10_intervals_above_48h
        else:
            IL10_intervals = IL10_intervals_below_48h
        IL10 = ctrl.Antecedent(np.arange(IL10_intervals[0], IL10_intervals[-1], .005), 'IL10')
        # print(IL10_intervals)
        IL10['Neg'] = fuzz.trimf(IL10.universe, [IL10_intervals[0], IL10_intervals[0],IL10_intervals[1]])
        IL10['Low'] = fuzz.trimf(IL10.universe, [IL10_intervals[0], IL10_intervals[1], IL10_intervals[2]])
        IL10['Stim'] = fuzz.trimf(IL10.universe, [IL10_intervals[1], IL10_intervals[2], IL10_intervals[3]])
        IL10['Det'] = fuzz.trapmf(IL10.universe, [IL10_intervals[2], IL10_intervals[3], IL10_intervals[-1], IL10_intervals[-1]])
        #// store
        self.antecedents['IL10']=IL10
    def define_rules(self):
        #// rules
        IL10 = self.antecedents['IL10']
        early_diff = self.consequents['early_diff']
        late_diff = self.consequents['late_diff']
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
        return outputs
class Fuzzy_IL8_IL1b(Fuzzy_controller):
    def __init__(self,params):
        super().__init__(params)
        self.define_antecedents()
        self.define_consequents()
        self.define_rules()
        self.reset()
    def reset(self):
        self.default_inputs = {'IL8':0,'IL1b':0}
    def define_antecedents(self):
        #// define antecedents
        intervals = [0,self.params['IL8_M'],100]
        IL8 = ctrl.Antecedent(np.arange(intervals[0], intervals[-1], .005), 'IL8')
        # print(IL10_intervals)
        IL8['Neg'] = fuzz.trimf(IL8.universe, [intervals[0], intervals[0],intervals[1]])
        IL8['Med'] = fuzz.trimf(IL8.universe, [intervals[0], intervals[1], intervals[2]])
        IL8['High'] = fuzz.trimf(IL8.universe, [intervals[1], intervals[2], intervals[2]])
        IL8['NNeg'] = fuzz.trapmf(IL8.universe, [intervals[0], intervals[1],intervals[-1],intervals[-1]])

        #// store
        self.antecedents['IL8']=IL8

        intervals = [0,10,self.params['IL1b_H'],200]
        IL1b = ctrl.Antecedent(np.arange(intervals[0], intervals[-1], .005), 'IL1b')
        IL1b['Neg'] = fuzz.trimf(IL1b.universe, [intervals[0], intervals[0],intervals[1]])
        IL1b['Stim'] = fuzz.trimf(IL1b.universe, [intervals[0], intervals[1], intervals[2]])
        IL1b['High'] = fuzz.trapmf(IL1b.universe, [intervals[1], intervals[2], intervals[3],intervals[3]])
        IL1b['NNeg'] = fuzz.trapmf(IL1b.universe, [intervals[0], intervals[1],intervals[-1],intervals[-1]])


        self.antecedents['IL1b']=IL1b

    def define_rules(self):
        #// rules
        IL8 = self.antecedents['IL8']
        IL1b = self.antecedents['IL1b']
        early_diff = self.consequents['early_diff']
        late_diff = self.consequents['late_diff']
        early_diff_rules = [
            # only IL8
            ctrl.Rule(IL1b['Neg'] & IL8['Neg'] , early_diff['M']),
            ctrl.Rule(IL1b['Neg'] & IL8['Med'] , early_diff['VH']),
            ctrl.Rule(IL1b['Neg'] & IL8['High'] , early_diff['EH']),
            # only IL1b
            ctrl.Rule(IL1b['Stim'] & IL8['Neg'] , early_diff['H']),
            ctrl.Rule(IL1b['High'] & IL8['Neg'] , early_diff['M']),
            # combined
            ctrl.Rule(IL1b['NNeg'] & IL8['NNeg'] , early_diff['VH'])            

        ]
        rules = early_diff_rules
        self.controler = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

class Fuzzy_TNFa(Fuzzy_controller):
    def __init__(self,params):
        super().__init__(params)
        self.define_antecedents()
        self.define_consequents()
        self.define_rules()
    def define_antecedents(self):
        #// define antecedents
        intervals = [0,1,10]
        factor = ctrl.Antecedent(np.arange(intervals[0], intervals[-1], .005), 'TNFa')
        # print(IL10_intervals)
        factor['Low'] = fuzz.trimf(factor.universe, [intervals[0], intervals[0],intervals[1]])
        factor['Med'] = fuzz.trimf(factor.universe, [intervals[0], intervals[1], intervals[2]])
        factor['High'] = fuzz.trimf(factor.universe, [intervals[1], intervals[2], intervals[2]])

        #// store
        self.antecedents['TNFa']=factor

    def define_consequents(self):
        #// define consequents
        range_value = np.arange(.5, 1, .01)
        early_diff = ctrl.Consequent(range_value, 'early_diff')
        late_diff = ctrl.Consequent(range_value, 'late_diff')
        
        #// define membership functions
        sigma = .05
        diff_intervals = [.5, 1]
        early_diff['M']=fuzz.gaussmf(range_value, diff_intervals[0], sigma)
        early_diff['H']=fuzz.gaussmf(range_value, diff_intervals[1], sigma)

        diff_intervals = [.5,1]
        late_diff['M']=fuzz.gaussmf(range_value, diff_intervals[0], sigma)
        late_diff['H']=fuzz.gaussmf(range_value, diff_intervals[1], sigma)
        #// Store
        self.consequents['early_diff'] = early_diff
        self.consequents['late_diff'] = late_diff

    def define_rules(self):
        #// rules
        factor = self.antecedents['TNFa']
        early_diff = self.consequents['early_diff']
        late_diff = self.consequents['late_diff']
        early_diff_rules = [
            ctrl.Rule(factor['Med'] , early_diff['H']),
            ctrl.Rule(factor['Low'] | factor['High'] , early_diff['M']),
        ]
        late_diff_rules = [
            ctrl.Rule(factor['Med'] , late_diff['H']),
            ctrl.Rule(factor['Low'] | factor['High'] , late_diff['M']),
        ]
        rules = early_diff_rules+late_diff_rules
        self.controler = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
        

class Fuzzy_Mg(Fuzzy_controller):
    def __init__(self,params):
        super().__init__(params)
        self.define_antecedents()
        self.define_consequents()
        self.define_rules()
    def define_antecedents(self):
        #// define antecedents
        neut = np.mean([self.params['Mg_S'],self.params['Mg_D']])
        intervals = [0,0.08,0.8,1.8,self.params['Mg_S'],neut,self.params['Mg_D'],60]
        factor = ctrl.Antecedent(np.arange(0, 60, .005), 'Mg')
  
        factor['Des_e'] = fuzz.trapmf(factor.universe, [intervals[0], intervals[0],intervals[1],intervals[2]])
        factor['Phy'] = fuzz.trimf(factor.universe, [intervals[1],intervals[2],intervals[4]])
        factor['Stim'] = fuzz.trimf(factor.universe, [intervals[2],intervals[4],intervals[5]])
        factor['Neut'] = fuzz.trimf(factor.universe, [intervals[4],intervals[5],intervals[6]])
        factor['Tox'] = fuzz.trapmf(factor.universe, [intervals[5],intervals[6],intervals[-1],intervals[-1]])
        factor['Des_l'] = fuzz.trapmf(factor.universe, [intervals[3],intervals[6],intervals[-1],intervals[-1]])
        factor['Adv_Des_l'] = fuzz.trapmf(factor.universe, [intervals[0],intervals[0],intervals[3],intervals[6]])

        #// store
        self.antecedents['Mg']=factor

    def define_consequents(self):
        #// define consequents
        early_range_value = np.arange(0, 1, .01)
        late_range_value = np.arange(0, .5, .01)
        early_diff = ctrl.Consequent(early_range_value, 'early_diff')
        late_diff = ctrl.Consequent(late_range_value, 'late_diff')
        
        #// define membership functions
        sigma = .05
        
        early_diff_intervals = [0,.5, 1]
        early_diff['L']=fuzz.gaussmf(early_range_value, early_diff_intervals[0], sigma)
        early_diff['M']=fuzz.gaussmf(early_range_value, early_diff_intervals[1], sigma)
        early_diff['H']=fuzz.gaussmf(early_range_value, early_diff_intervals[2], sigma)
        # early_diff.view()
        late_diff_intervals = [0,.5]
        late_diff['L']=fuzz.gaussmf(late_range_value, late_diff_intervals[0], sigma)
        late_diff['M']=fuzz.gaussmf(late_range_value, late_diff_intervals[1], sigma)
        # late_diff.view()
        #// Store
        self.consequents['early_diff'] = early_diff
        self.consequents['late_diff'] = late_diff

    def define_rules(self):
        #// rules
        factor = self.antecedents['Mg']
        early_diff = self.consequents['early_diff']
        late_diff = self.consequents['late_diff']
        early_diff_rules = [
            ctrl.Rule(factor['Stim'] , early_diff['H']),
            ctrl.Rule(factor['Phy'] | factor['Neut'] , early_diff['M']),
            ctrl.Rule(factor['Des_e'] | factor['Tox'] , early_diff['L'])
        ]
        late_diff_rules = [
            ctrl.Rule(factor['Des_l'] , late_diff['L']),
            ctrl.Rule(factor['Adv_Des_l'] , late_diff['M']),
        ]
        rules = early_diff_rules+late_diff_rules
        self.controler = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
        
        
