
observations = {
	# 'studies':['Qiao_2021_Mg'],
	# 'studies': ['Qiao_2021_IL8_IL1b','Qiao_2021_IL8','Qiao_2021_IL1b'],
	# 'studies':['Ber_2016'],
	# 'studies':['Chen_2018'],
	'studies':['Valles_2020_IL10'],
	# 'studies':['Valles_2020_TNFa'],
	# 'studies':['Valles_2020_TNFa','Valles_2020_IL10','Chen_2018','Qiao_2021_IL8_IL1b','Qiao_2021_IL8','Qiao_2021_IL1b'],


	'Chen_2018':{# the effect of IL10 on ALP and ARS
		'exposure_time':9*24, #when this is none, the cells are exposed to the stimuli the whole time
		'culture_volume':None, #ml
		'experiment_period':9, # days
		'measurement_scheme':{
			'ALP': [3*24], #hour
			'ARS': [9*24]
		},
		'IDs': ['ctr','IL10_.01','IL10_.1','IL10_1','IL10_10','IL10_100'],
		# 'IDs': ['ctr','IL10_.1','IL10_1','IL10_100'],
		# 'IDs': ['ctr'],
		'ctr':{
			'inputs':{
						"IL10": 0
					},
			"expectations": {
				"ALP": {
					'mean':[2],
					'std': [0]
				},
				"ARS": {
					'mean':[1],
					'std': [.1]
				},
			}

		},
		'IL10_.01':{
			'inputs':{
						"IL10": 0.01
					},
			"expectations": {
				"ALP": {
					'mean':[2.5],
					'std': [.5]
				},
				"ARS": {
					'mean':[1.7],
					'std': [.15]
				},
			}

		},
		'IL10_.1':{
			'inputs':{
						"IL10": 0.1
					},
			"expectations": {
				"ALP": {
					'mean':[5.6],
					'std': [.2]
				},
				"ARS": {
					'mean':[4],
					'std': [.6]
				},
			}

		},
		'IL10_1':{
			'inputs':{
						"IL10": 1
					},
			"expectations": {
				"ALP": {
					'mean': [4.1],
					'std': [.5]
				},
				"ARS": {
					'mean': [3],
					'std': [.4]
				},
			}

		},
		'IL10_10':{
			'inputs':{
						"IL10": 10
					},
			"expectations": {
				"ALP": {
					'mean': [1.2],
					'std': [.3]
				},
				"ARS": {
					'mean': [0.5],
					'std': [.1]
				},
			}

		},
		'IL10_100':{
			'inputs':{
						"IL10": 100
					},
			"expectations": {
				"ALP": {
					'mean': [1.5],
					'std': [.15]
				},
				"ARS": {
					'mean': [0.4],
					'std': [.15]
				},
			}

		},
	},
	'Valles_2020_IL10':{# the effect of IL10 on ALP and ARS
		'exposure_time':48, #hours
		'culture_volume':2, #ml
		'experiment_period':21, # days
		'measurement_scheme':{
			'ALP': [14*24], #hour
			'ARS': [21*24]
		},
		'IDs': ['ctr','IL10_.1','IL10_1','IL10_10'],
		# 'IDs': ['ctr','IL10_1','IL10_10'],
		# 'IDs': ['ctr','IL10_10'],
		'ctr':{
			'inputs':{
						"IL10": 0
					},
			"expectations": {
				"ALP": {
					'mean':[200],
					'std': [40]
				},
				"ARS": {
					'mean':[550],
					'std': [50]
				},
			}

		},
		'IL10_.1':{
			'inputs':{
						"IL10": 0.1
					},
			"expectations": {
				"ALP": {
					'mean':[290],
					'std': [25]
				},
				"ARS": {
					'mean':[550],
					'std': [70]
				},
			}

		},
		'IL10_1':{
			'inputs':{
						"IL10": 1
					},
			"expectations": {
				"ALP": {
					'mean':[350],
					'std': [70]
				},
				"ARS": {
					'mean':[800],
					'std': [60]
				},
			}

		},
		'IL10_10':{
			'inputs':{
						"IL10": 10
					},
			"expectations": {
				"ALP": {
					'mean':[420],
					'std': [80]
				},
				"ARS": {
					'mean':[850],
					'std': [100]
				},
			}

		}

	},
	'Valles_2020_TNFa':{# the effect of TNF-a on ALP and ARS
		'exposure_time':48, #hours
		'culture_volume':2, #ml
		'experiment_period':21, # days
		'measurement_scheme':{
			'ALP': [14*24], #hour
			'ARS': [21*24]
		},
		'IDs': ['ctr','TNFa_.1','TNFa_1','TNFa_10'],
		'ctr':{
			'inputs':{
						"TNFa": 0 #ng/ml
					},
			"expectations": {
				"ALP": {
					'mean':[200],
					'std': [40]
				},
				"ARS": {
					'mean':[550],
					'std': [50]
				},
			}

		},
		'TNFa_.1':{
			'inputs':{
						"TNFa": .1 #ng/ml
					},
			"expectations": {
				"ALP": {
					'mean':[180],
					'std': [45]
				},
				"ARS": {
					'mean':[570],
					'std': [55]
				},
			}

		},
		'TNFa_1':{
			'inputs':{
						"TNFa": 1 #ng/ml
					},
			"expectations": {
				"ALP": {
					'mean':[300],
					'std': [45]
				},
				"ARS": {
					'mean':[670],
					'std': [50]
				},
			}

		},
		'TNFa_10':{
			'inputs':{
						"TNFa": 10 #ng/ml
					},
			"expectations": {
				"ALP": {
					'mean':[200],
					'std': [50]
				},
				"ARS": {
					'mean':[520],
					'std': [50]
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
	'Qiao_2021_IL8':{# the effect of IL8 on ALP
		'exposure_time':9*24,
		'culture_volume':None, #ml
		# 'experiment_period':9, # days
		'measurement_scheme':{
			'ALP': [9*24] #hour
		},
		'IDs': ['ctr','IL8_1','IL8_10','IL8_100'],
		'ctr':{
			'inputs':{
						"IL8": 0
					},
			"expectations": {
				"ALP": {
					'mean':[12],
					'std': [5]
				}
			}

		},
		'IL8_1':{
			'inputs':{
						"IL8": 1
					},
			"expectations": {
				"ALP": {
					'mean':[21],
					'std': [5]
				}
			}

		},
		'IL8_10':{
			'inputs':{
						"IL8": 10
					},
			"expectations": {
				"ALP": {
					'mean':[45],
					'std': [15]
				}
			}

		},
		'IL8_100':{
			'inputs':{
						"IL8": 100
					},
			"expectations": {
				"ALP": {
					'mean':[115],
					'std': [10]
				}
			}

		}
	},
	'Qiao_2021_IL1b':{# the effect of IL8 on ALP
		'exposure_time':9*24,
		'culture_volume':None, #ml
		# 'experiment_period':9, # days
		'measurement_scheme':{
			'ALP': [9*24] #hour
		},
		'IDs': ['ctr','IL1b_1','IL1b_10','IL1b_100'],
		'ctr':{
			'inputs':{
						"IL1b": 0
					},
			"expectations": {
				"ALP": {
					'mean':[11],
					'std': [5]
				}
			}

		},
		'IL1b_1':{
			'inputs':{
						"IL1b": 1
					},
			"expectations": {
				"ALP": {
					'mean':[30],
					'std': [5]
				}
			}

		},
		'IL1b_10':{
			'inputs':{
						"IL1b": 10
					},
			"expectations": {
				"ALP": {
					'mean':[39],
					'std': [8]
				}
			}

		},
		'IL1b_100':{
			'inputs':{
						"IL1b": 100
					},
			"expectations": {
				"ALP": {
					'mean':[22],
					'std': [6]
				}
			}

		}
	},
	'Qiao_2021_IL8_IL1b':{# the synnergic effect of IL8 and IL1b on ALP
		'exposure_time':9*24,
		'culture_volume':None, #ml
		# 'experiment_period':9, # days
		'measurement_scheme':{
			'ALP': [9*24] #hour
		},
		'IDs': ['ctr','IL1b_IL8'],
		'ctr':{
			'inputs':{
						"IL1b": 0,
						"IL8": 0
					},
			"expectations": {
				"ALP": {
					'mean':[11],
					'std': [5]
				}
			}

		},
		'IL1b_IL8':{
			'inputs':{
						"IL1b": 100,
						"IL8": 100
					},
			"expectations": {
				"ALP": {
					'mean':[41],
					'std': [8]
				}
			}

		}
	},
	'Ber_2016':{ # the effect of Mg on ALP and OC
		'exposure_time':21*24,
		'culture_volume':None, #ml
		'cell_type':'HUCPV',
		# 'experiment_period':7, # days
		'measurement_scheme':{
			'ALP': [7*24,14*24,21*24], #hour
			'OC':[7*24,14*24,21*24]
		},
		'IDs': ['Mg_.8','Mg_5'],
		'Mg_.8':{
			'inputs':{
						"Mg": 0.8
					},
			"expectations": {
				"ALP": {
					'mean':[0.30,0.53,0.57],
					'std': [0,0,0]
				},
				'OC':{
					'mean':[0.53,0.71,0.8],
					'std': [0,0,0]
				}
			}

		},
		'Mg_5':{
			'inputs':{
						"Mg": 5
					},
			"expectations": {
				"ALP": {
					'mean':[0.34,0.39, 0.61],
					'std': [0,0,0]
				},
				'OC':{
					'mean':[0.28,0.22,0.27],
					'std': [0,0,0]
				}
			}

		},
	},
	'Qiao_2021_Mg':{# the effect of Mg on ALP
		'exposure_time':7*24,
		'culture_volume':None, #ml
		# 'experiment_period':7, # days
		'measurement_scheme':{
			'ALP': [3*24,7*24] #hour
		},
		'IDs': ['Mg_.08','Mg_.8','Mg_8'],
		# 'IDs': ['Mg_10'],
		'Mg_.08':{
			'inputs':{
						"Mg": 0.08
					},
			"expectations": {
				"ALP": {
					'mean':[7,10],
					'std': [2,3]
				}
			}

		},
		'Mg_.8':{
			'inputs':{
						"Mg": 0.8
					},
			"expectations": {
				"ALP": {
					'mean':[9,15],
					'std': [2,3]
				}
			}

		},
		'Mg_8':{
			'inputs':{
						"Mg": 8
					},
			"expectations": {
				"ALP": {
					'mean':[13,20],
					'std': [4,3]
				}
			}

		},

	},

	"scale": 1,
}
import json
# with open('observations.json','w') as file:
# 	file.write(json.dumps(observations,indent=4))
