import numpy as np
import FUZZY.define_mfs as define_mfs
import FUZZY.calculate as calculate
import FUZZY.find_mfs as find_mfs
import FUZZY.implication as implication
import FUZZY.fuzzyfication as fuzzyfication
import FUZZY.defuzzyfication as defuzzyfication
import FUZZY.automatic as automatic
import os,sys



class this_automatic(object):
	def __init__(self, control):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules

		self.ctrl = control

	def compute(self, type_fuzzy):
		find_mfs_ = find_mfs.this_find_mfs(self.ctrl)
		f = find_mfs_.find_coordinate()

		impli = implication.this_implication(self.ctrl, f)
		imps = impli.implication_rules()

		fuz = fuzzyfication.this_fuzzyfication(self.ctrl, f, imps)
		fz = fuz.start()
		imp_min = impli.min(fz)
		imp_max = impli.max(imp_min)

		defz = 0
		defz_sugeno = 0
		try:
			defuz = defuzzyfication.this_defuzzyfication(self.ctrl, imp_max)
			defz = defuz.main()
		except Exception as e:
			pass

		try:
			defuz_sugeno = defuzzyfication.defuzzyfication_sugeno(self.ctrl, imp_min)
			defz_sugeno = defuz_sugeno.main()
		except Exception as e:
			pass

		return defz, defz_sugeno