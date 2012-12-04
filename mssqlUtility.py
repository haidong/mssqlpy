import pyodbc

def getVersionNumber(instance):
	try:
		cn = pyodbc.connect("DRIVER={SQL Server};SERVER=%s;DATABASE=master;Trusted_Connection=yes" % instance) 
		cursor = cn.cursor()
		cursor.execute("SELECT cast(SERVERPROPERTY('productversion') AS VARCHAR) AS versionNumber")
		row = cursor.fetchone()
		return row.versionNumber
	except:
		return None

def cursorResultsPrettyPrint(cursor, data=None, check_row_lengths=True):
	"""This function returns the results neatly formatted. Great for print to command line and as email body"""
	if not data:
		data = cursor.fetchall( )
	names = [  ]
	lengths = [  ]
	rules = [  ]
	for col, field_description in enumerate(cursor.description):
		field_name = field_description[0]
		names.append(field_name)
		field_length = field_description[2] or 12
		field_length = max(field_length, len(field_name))
		if check_row_lengths:
			# double-check field length, if it's unreliable
			data_length = max([ len(str(`row[col]`)) for row in data ])
			field_length = max(field_length, data_length)
		lengths.append(field_length)
		rules.append('-' * field_length)
	format = " ".join(["%%-%ss" % l for l in lengths])
	result = [ format % tuple(names), format % tuple(rules) ]
	for row in data:
		result.append(format % tuple(row))
	return "\n".join(result)
