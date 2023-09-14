import database.conn as connection
import helpers.config as keys
import datetime

class this_mpu605:
	def __init__(self):
		self.conn = connection.connect()
		self.now = datetime.datetime.now()


	def add(self, ax, ay, az, gx, gy, gz):
		get = self.conn.connect()
		query = f"INSERT INTO mpu605 (AX, AY, AZ, GX, GY, GZ, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		val = (ax, ay, az, gx, gy, gz, self.now)
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
		query = f"SELECT * FROM mpu605"
		get[1].execute(query)
		result = get[1].fetchall()
		if result != None:
			return result

		else:
			return False
	