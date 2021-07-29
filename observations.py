observations = {
	"IDs": ['MSC_0_0','MSC_0_.1','MSC_0_1','MSC_1_0','MSC_1_.1','MSC_1_1','MSC_10_0','MSC_10_.1','MSC_10_1'],
	# "IDs": ['MSC_0_0','MSC_1_0','MSC_10_0'],

	"MSC_0_0": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 0, #ng/ml
				"IL10": 0
			}
		},

		"expectations": {			
			"IL6": 0.5, #ng/ml
			"PGE2": 0.03
		}
	},
	"MSC_0_.1": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 0, #ng/ml
				"IL10": .1
			}
		},

		"expectations": {			
			"IL6": 0.45, #ng/ml
			"PGE2": 0.028
		}
	},
	"MSC_0_1": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 0, #ng/ml
				"IL10": 1
			}
		},

		"expectations": {			
			"IL6": 0.48, #ng/ml
			"PGE2": 0.026
		}
	},
	"MSC_1_0": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 1, #ng/ml
				"IL10": 0
			}
		},

		"expectations": {			
			"IL6": 0.76, #ng/ml
			"PGE2": 0.09
		}
	},
	"MSC_1_.1": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 1, #ng/ml
				"IL10": .1
			}
		},

		"expectations": {			
			"IL6": 0.74, #ng/ml
			"PGE2": 0.1
		}
	},
	"MSC_1_1": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 1, #ng/ml
				"IL10": 1
			}
		},

		"expectations": {			
			"IL6": 0.64, #ng/ml
			"PGE2": 0.12
		}
	},
	"MSC_10_0": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 10, #ng/ml
				"IL10": 0
			}
		},

		"expectations": {			
			"IL6": 1.25, #ng/ml
			"PGE2": 0.13
		}
	},
	"MSC_10_.1": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 10, #ng/ml
				"IL10": .1
			}
		},

		"expectations": {			
			"IL6": 1.3, #ng/ml
			"PGE2": 0.14
		}
	},
	"MSC_10_1": {
		"setup": {
			'duration': 48, #h
			'inputs':{
				"TNFa": 10, #ng/ml
				"IL10": 1
			}
		},

		"expectations": {			
			"IL6": 1.15, #ng/ml
			"PGE2": 0.175
		}
	},

	"scale": 1,
}
import json
with open('observations.json','w') as file:
	file.write(json.dumps(observations,indent=4))
