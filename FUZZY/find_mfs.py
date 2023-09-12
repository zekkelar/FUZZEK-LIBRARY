import numpy as np

class this_find_mfs():
	def __init__(self, control):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules

	def find_coordinate(self):
		key_and_value = dict()
		for key in self.Antecendent:
			key_and_value[key]=((self.Antecendent[key]['input_value']))

		#{'curah_hujan':500}
		_result_find_mfs = dict()
		for key in key_and_value:
			_result_find_mfs[key] = []
			for x in self.Antecendent[key]:
				if 'input_value' in x or 'range_domain' in x or 'Type-Plot' in x:
					pass
				else:
					first_index = float(self.Antecendent[key][x][0])
					last_index = float(self.Antecendent[key][x][-1])

					if type(first_index)==float:
						numpii = np.arange(first_index, last_index+1, 0.1)
					else:
						numpii = np.arange(first_index, last_index+1, 1)
					for find_ in numpii:
						if str(key_and_value[key]) == str(round(find_, 2)):
							_result_find_mfs[key].append(x)
				
		return _result_find_mfs

	