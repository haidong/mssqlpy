import pyodbc, argparse
from mssqlUtility import cursorResultsPrettyPrint

parser = argparse.ArgumentParser(description="Get an instance's database file information such as their names and drive location")
parser.add_argument('-S', '--server', help='Instance you wish to connect to. myImportantInstance is the default if not specified', dest='instance', default='myImportantInstance')

argList = parser.parse_args()

cn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=master;Trusted_Connection=yes' % argList.instance)
cursor = cn.cursor()
cursor.execute("select name, database_id from sys.databases ")
rows = cursor.fetchall()
sql = ''
for row in rows:
	sql = sql + ("select '%s' dbName, type_desc, physical_name from %s.sys.database_files" % (row.name, row.name)) + ' union all '

#Remove the last union all because a sql statement ends with union all is not valid
sql = sql.rpartition('union all ')[0]
cursor.execute(sql)
l1rows = cursor.fetchall()
print cursorResultsPrettyPrint(cursor, l1rows, True)
