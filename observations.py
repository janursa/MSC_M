observations = {
	'studies':['Chen_2018'],
	# 'studies':['Saldana_2019','Valles_2020_part1','Chen_2018'],
	'Chen_2018':{# the effect of Il10 on ALP and ARS
		'exposure_period':9*24, #when this is none, the cells are exposed to the stimuli the whole time
		'culture_volume':None, #ml
		'experiment_period':9, # days
		# 'measurement_scheme':{
		# 	'ALP': 3, #day
		# 	'ARS': 9
		# },
		'measurement_scheme':{
			# 'ALP': 3, #day
			'ARS': 9
		},
		# 'IDs': ['ctr','IL10_.01','IL10_.1','IL10_1','IL10_10','IL10_100'],
		'IDs': ['ctr','IL10_.01','IL10_.1','IL10_100'],
		# 'IDs': ['ctr'],
		'ctr':{
			'inputs':{
						"IL10": 0
					},
			"expectations": {			
				"ALP": {
					'mean':2, 
					'std': 0
				},
				"ARS": {
					'mean':1, 
					'std': .1
				},
			}

		},
		'IL10_.01':{
			'inputs':{
						"IL10": 0.01
					},
			"expectations": {			
				"ALP": {
					'mean':2.5, 
					'std': .5
				},
				"ARS": {
					'mean':1.7, 
					'std': .15
				},
			}

		},
		'IL10_.1':{
			'inputs':{
						"IL10": 0.1
					},
			"expectations": {			
				"ALP": {
					'mean':5.6, 
					'std': .2
				},
				"ARS": {
					'mean':4, 
					'std': .6
				},
			}

		},
		'IL10_1':{
			'inputs':{
						"IL10": 1
					},
			"expectations": {			
				"ALP": {
					'mean': 4.1, 
					'std': .5
				},
				"ARS": {
					'mean': 3, 
					'std': .4
				},
			}

		},
		'IL10_10':{
			'inputs':{
						"IL10": 10
					},
			"expectations": {			
				"ALP": {
					'mean': 1.2, 
					'std': .3
				},
				"ARS": {
					'mean': 0.5, 
					'std': .1
				},
			}

		},
		'IL10_100':{
			'inputs':{
						"IL10": 100
					},
			"expectations": {			
				"ALP": {
					'mean': 1.5, 
					'std': .15
				},
				"ARS": {
					'mean': 0.4, 
					'std': .15
				},
			}

		},
	},
	'Valles_2020_part1':{# the effect of TNF-a and IL10 on ALP and ARS
		'exposure_period':48, #hours
		'culture_volume':2, #ml
		'experiment_period':21, # days
		'measurement_scheme':{
			'ALP': 14, #day
			'ARS': 21
		},
		
		# 'IDs': ['ctr','TNFa_.1','TNFa_1','TNFa_10','IL10_.1','IL10_1','IL10_10'],
		'IDs': ['ctr','IL10_.1','IL10_1','IL10_10'],
		'ctr':{
			'inputs':{
						"TNFa": 0, #ng/ml
						"IL10": 0
					},
			"expectations": {			
				"ALP": {
					'mean':200, 
					'std': 40
				},
				"ARS": {
					'mean':550, 
					'std': 50
				},
			}

		},
		'TNFa_.1':{
			'inputs':{
						"TNFa": .1, #ng/ml
						"IL10": 0
					},
			"expectations": {			
				"ALP": {
					'mean':180, 
					'std': 45
				},
				"ARS": {
					'mean':570, 
					'std': 55
				},
			}

		},
		'TNFa_1':{
			'inputs':{
						"TNFa": 1, #ng/ml
						"IL10": 0
					},
			"expectations": {			
				"ALP": {
					'mean':300, 
					'std': 45
				},
				"ARS": {
					'mean':670, 
					'std': 50
				},
			}

		},
		'TNFa_10':{
			'inputs':{
						"TNFa": 10, #ng/ml
						"IL10": 0
					},
			"expectations": {			
				"ALP": {
					'mean':200, 
					'std': 50
				},
				"ARS": {
					'mean':520, 
					'std': 50
				},
			}

		},
		'IL10_.1':{
			'inputs':{
						"TNFa": 0, #ng/ml
						"IL10": 0.1
					},
			"expectations": {			
				"ALP": {
					'mean':290, 
					'std': 25
				},
				"ARS": {
					'mean':550, 
					'std': 70
				},
			}

		},
		'IL10_1':{
			'inputs':{
						"TNFa": 0, #ng/ml
						"IL10": 1
					},
			"expectations": {			
				"ALP": {
					'mean':350, 
					'std': 70
				},
				"ARS": {
					'mean':800, 
					'std': 60
				},
			}

		},
		'IL10_10':{
			'inputs':{
						"TNFa": 0, #ng/ml
						"IL10": 10
					},
			"expectations": {			
				"ALP": {
					'mean':420, 
					'std': 80
				},
				"ARS": {
					'mean':850, 
					'std': 100
				},
			}

		}

	},
	'Saldana_2019':{ # the effect of TNF-a and IL10 on IL6 and PGE2
		"IDs": ['MSC_0_0','MSC_0_.1','MSC_0_1','MSC_1_0','MSC_1_.1','MSC_1_1','MSC_10_0','MSC_10_.1','MSC_10_1'],
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
			}
	},

	"scale": 1,
}
import json
with open('observations.json','w') as file:
	file.write(json.dumps(observations,indent=4))
