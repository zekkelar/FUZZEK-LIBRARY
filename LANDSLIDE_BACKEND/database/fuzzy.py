import database.conn as connection
import helpers.config as keys
import datetime

class this_fuzzy:
	def __init__(self):
		self.conn = connection.connect()
		self.now = datetime.datetime.now()

	def upload(self,curah_hujan,soil,gyro,temperature,potensiometer,defuz, defuz_sugeno):
		get = self.conn.connect()
		query = f"INSERT INTO fuzzy (curah_hujan,soil,gyro,temperature,potensiometer,fuzzy_output,fuzzy_output_sugeno,datetime) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
		val = (curah_hujan,soil,gyro,temperature,potensiometer,defuz,defuz_sugeno, self.now)
		try:
			get[1].execute(query, val)
			get[0].commit()
			get[0].close()
			return True
		except Exception as e:
			print(e)
			return False

	def view(self):
		get = self.conn.connect()
		query = f"SELECT * FROM fuzzy"
		get[1].execute(query)
		result = get[1].fetchall()
		if result!=None:
			return result
		else:
			return False