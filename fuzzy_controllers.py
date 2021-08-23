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
    def define_antecedents(self):
        pass
    def define_consequents(self):
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
        self.consequents['early_diff'] = early_diff
        self.consequents['late_diff'] = late_diff
    def define_rules(self):
        pass
    def forward(self,inputs):
        for key,value in inputs.items():
            self.controler.input[key] = value
        self.controler.compute()
        # for item in self.consequents:
        #     item.view(sim=self.controler)
        outputs = self.controler.output
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
        IL10_intervals_below_48h= [0,0.01,10,self.params['IL10_det'],100]
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
#         IL10.view()
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
#         print(outputs)
        # outputs['early_diff'] = outputs['diff'] 
        # outputs['late_diff'] = outputs['diff'] 
        return outputs
class Fuzzy_IL8(Fuzzy_controller):
    def __init__(self,params):
        super().__init__(params)
        self.define_antecedents()
        self.define_consequents()
        self.define_rules()
    def define_antecedents(self):
        #// define antecedents
        intervals = [0,self.params['IL8_M'],100]
        IL8 = ctrl.Antecedent(np.arange(intervals[0], intervals[-1], .005), 'IL8')
        # print(IL10_intervals)
        IL8['Low'] = fuzz.trimf(IL8.universe, [intervals[0], intervals[0],intervals[1]])
        IL8['Med'] = fuzz.trimf(IL8.universe, [intervals[0], intervals[1], intervals[2]])
        IL8['High'] = fuzz.trimf(IL8.universe, [intervals[1], intervals[2], intervals[2]])
        #// store
        self.antecedents['IL8']=IL8
        # IL8.view()

    def define_rules(self):
        #// rules
        IL8 = self.antecedents['IL8']
        early_diff = self.consequents['early_diff']
        late_diff = self.consequents['late_diff']
        early_diff_rules = [
            ctrl.Rule(IL8['High'] , early_diff['VH']),
            ctrl.Rule(IL8['Med'] , early_diff['H']),
            ctrl.Rule(IL8['Low'] , early_diff['M'])
        ]
        # late_diff_rules = [
        #     ctrl.Rule(IL8['Low'] or IL8['Med'] or IL8['High'] , late_diff['L']),
        #     ctrl.Rule(IL8['Low'] or IL8['Med'] or IL8['High'] , late_diff['M']),
        #     ctrl.Rule(IL8['Low'] or IL8['Med'] or IL8['High'] , late_diff['H'])
        # ]
        late_diff_rules = [
            ctrl.Rule(IL8['Low'] , late_diff['VH']),
            ctrl.Rule(IL8['Med'] , late_diff['H']),
            ctrl.Rule(IL8['High'] , late_diff['M']),
            ctrl.Rule(IL8['Low'] , late_diff['L'])
        ]
        rules = early_diff_rules+late_diff_rules
        self.controler = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))
        
    