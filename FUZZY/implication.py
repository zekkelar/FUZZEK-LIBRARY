from itertools import product

class this_implication(object):
	def __init__(self, control, mfs_found):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules

		self.define_mfs = mfs_found

	
	def match_implies_with_rules(self,implies, rules):
		matched_results = {}

		for result_key, conditions_list in implies.items():
			matched_rules = []

			for conditions in conditions_list:
				conditions_split = [cond.split('|') for cond in conditions]
				matched_rule = None

				if all(len(cond_split) == 2 for cond_split in conditions_split):
					conditions_dict = dict(conditions_split)
					for rule_key, rule_data in rules.items():
						if all(field in rule_data and rule_data[field] == value for field, value in conditions_dict.items()):
							matched_rule = rule_key
							break

				if matched_rule:
					matched_rules.append(matched_rule)

			matched_results[result_key] = matched_rules
		return matched_results


	def implication_rules(self):		
		#"{'1': [('curah_hujan|sedang', 'soil|normal')], '2': [('curah_hujan|sedang', 'soil|basah')], '3': [('curah_hujan|hujan', 'soil|normal')], '4': [('curah_hujan|hujan', 'soil|basah')]}"
		formatted_dict = {}
		combinations = list(product(*[[f"{key}|{value}" for value in values] for key, values in self.define_mfs.items()]))
		#print(f'Combination : {combinations}')
		for idx, pair in enumerate(combinations, start=1):
			#print(pair)
			formatted_dict[str(idx)] = [pair]

		match = self.match_implies_with_rules(formatted_dict, self.Rules)
		for key, val in match.items():
			formatted_dict[key].append(f'RulesIntegration:{val[0]}')
		return (formatted_dict)

	def min(self, fuzzyfication):
		"""
		fungsi untuk mencari nilai paling minimum antar tiap parameter yang sudah di
		fuzzyfikasi
		
		winner:minimum-value
		"""
		for num in fuzzyfication:
			fuzzyfication[num].update({'winner':{}})
			number_temp = []
			for name_mf in fuzzyfication[num]:
				for val in fuzzyfication[num][name_mf]:
					if name_mf == 'RulesIntegration':
						pass
					else:
						number_temp.append(fuzzyfication[num][name_mf][val])	

			fuzzyfication[num]['winner'] = min(number_temp)
		return fuzzyfication

	def process_results(self,results):
		processed_results = {}

		for result_key, result_data in results.items():
			rules_integration = result_data['RulesIntegration']
			winner = result_data['winner']

			if rules_integration not in processed_results:
				processed_results[rules_integration] = result_data
			else:
				existing_winner = processed_results[rules_integration]['winner']
				if winner > existing_winner:
					processed_results[rules_integration] = result_data

		unique_processed_results = {}
		for rules_integration, result_data in processed_results.items():
			if result_data['winner'] not in unique_processed_results.values():
				unique_processed_results[rules_integration] = result_data

		return unique_processed_results

	def max(self, min_):
		"""
		fungsi ini untuk mencari nilai maximumnya
		dan jika memiliki nilai yang sama dan juga output yang sama, akan diambil nilai max nya
		"""
		filtered_data = {k: v for k, v in min_.items() if v['winner'] != 0}
		for key,val in filtered_data.items():
			for key_, val in (self.Rules[val['RulesIntegration']]['output'].items()):
				filtered_data[key].update({'RulesIntegration':val})

		filter_max = self.process_results(filtered_data)
		return(filter_max)
