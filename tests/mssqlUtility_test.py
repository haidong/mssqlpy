import pyodbc, unittest, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mssqlUtility'))
import mssqlUtility

class mssqlUtilityTest(unittest.TestCase):

	def test_getVersionNumber_server1(self):
		self.assertEqual(mssqlUtility.getVersionNumber("myTestInstance"), "10.50.2789.0")
	def test_getVersionNumber_NonExistent(self):
		self.assertEqual(mssqlUtility.getVersionNumber("junk"), None)
	def test_cursorResultsPrettyPrint(self):
		cn = pyodbc.connect("DRIVER={SQL Server};SERVER=myTestServer;DATABASE=master;Trusted_Connection=yes") 
		cursor = cn.cursor()
		cursor.execute("select name from sys.databases")
		self.assertIn("master", mssqlUtility.cursorResultsPrettyPrint(cursor))

