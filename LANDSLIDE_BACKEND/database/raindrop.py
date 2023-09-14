import database.conn as connection
import helpers.config as keys
import datetime

class this_raindrop:
	def __init__(self):
		self.conn = connection.connect()
		self.now = datetime.datetime.now()


	def add(self, value):
		get = self.conn.connect()
		query = f"INSERT INTO raindrop (value, datetime) VALUES (%s, %s)"
		val = (value, self.now)
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
		query = f"SELECT * FROM raindrop"
		get[1].execute(query)
		result = get[1].fetchall()
		if result != None:
			return result
		else:
			return False
	

	