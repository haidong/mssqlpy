import pyodbc, argparse
from mssqlUtility import cursorResultsPrettyPrint

def objectMatch(wildcardSearch, objectNamePattern, dbName, cn):
	if wildcardSearch:
		sql = "select '%s' as dbName, s.name schema_name, o.name, o.type from %s.sys.objects o inner join %s.sys.schemas s on o.schema_id = s.schema_id where o.name like '%%%s%%\' order by dbname, schema_name, o.name" % (dbName, dbName, dbName, objectNamePattern)
		cursor = cn.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		if len(rows) > 0:
			print cursorResultsPrettyPrint(cursor, rows, True)
	else:
		sql = "select '%s' as dbName, s.name schema_name, o.name, o.type from %s.sys.objects o inner join %s.sys.schemas s on o.schema_id = s.schema_id where o.name = '%s' order by dbname, schema_name, o.name" % (dbName, dbName, dbName, objectNamePattern)
		cursor = cn.cursor()
		cursor.execute(sql)
		rows = cursor.fetchall()
		if len(rows) > 0:
			print cursorResultsPrettyPrint(cursor, rows, True)

parser = argparse.ArgumentParser(description='SQL Server object search. Case insensitive')
parser.add_argument('-S', '--server', help='Instance you wish to connect to. myImportantInstance is the default if not specified', dest='instance', default='myImportantInstance')
parser.add_argument('-w', help='Wildcard search indicator. If specified, LIKE clause will be used for pattern matching. Otherwise it will look for an exact match. Exact match is default', action="store_true", dest='wild', default=False)
parser.add_argument('-d', '--database', help='Database(s) you want to search in. If more than one, separate them by comma only. It will search all databases by default', action="store", dest="dbs")
parser.add_argument('objectNamePattern', help='Object name pattern you want to search for', action="store")

argList = parser.parse_args()

try:
	cn = pyodbc.connect("DRIVER={SQL Server};SERVER=%s;DATABASE=master;Trusted_Connection=yes" % argList.instance)
except:
	print "Couldn't connect to %s. It is down or you might have had a typo." % argList.instance

if argList.dbs is None:
	cursor = cn.cursor()
	cursor.execute("select name from sys.databases where state = 0")
	rows = cursor.fetchall()
	for row in rows:
		objectMatch(argList.wild, argList.objectNamePattern, row.name, cn)
else:
	dbs = argList.dbs.split(',')
	for db in dbs:
		objectMatch(argList.wild, argList.objectNamePattern, db, cn)
