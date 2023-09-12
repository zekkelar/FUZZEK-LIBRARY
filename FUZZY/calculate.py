class this_calculate(object):
	def __init__(self, control, name_mf, input):
		control.Antecendent[name_mf].update({f'input_value':f'{float(input)}'})

