import argparse, pyodbc
from datetime import datetime, timedelta
from allPlatUtility import sendEmail
from mssqlUtility import cursorResultsPrettyPrint

parser = argparse.ArgumentParser(description="Check yesterday's SQL Server job status")
parser.add_argument('-f', '--fileInput', help='The presence of this parameter indicates server names come from a file',  action='store_true', default=False, dest='fileInput')
parser.add_argument('-i', '--input', help='When -f is present, please provide the name of the file that contains a list of servers, each on its own line. Otherwise, please type a list of servers, separated by comma.',  required=True, dest='iInput')

argList = parser.parse_args()

if argList.fileInput:
	text_file = open("%s" % argList.iInput, "r")
	serverList = text_file.readlines()
else:
	serverList = argList.iInput.split(',')

yesterday = datetime.now() - timedelta(days=1) 
yesterday = yesterday.strftime('%Y%m%d')

sql = """select sj.name jobName, case sjh.run_status
						when 1 then 'Success'
						when 2 then 'Retry'
						when 3 then 'Cancelled'
						when 4 then 'In Progress'
						when 0 then 'Failed'
						End
						 as 'runStatus',sjh.run_date as 'runDate',
CASE len(run_time)
		WHEN 1 THEN cast('00:00:0'
				+ cast(run_time as char) as char (8))
		WHEN 2 THEN cast('00:00:'
				+ cast(run_time as char) as char (8))
		WHEN 3 THEN cast('00:0'
				+ Left(right(run_time,3),1)
				+':' + right(run_time,2) as char (8))
		WHEN 4 THEN cast('00:'
				+ Left(right(run_time,4),2)
				+':' + right(run_time,2) as char (8))
		WHEN 5 THEN cast('0'
				+ Left(right(run_time,5),1)
				+':' + Left(right(run_time,4),2)
				+':' + right(run_time,2) as char (8))
		WHEN 6 THEN cast(Left(right(run_time,6),2)
				+':' + Left(right(run_time,4),2)
				+':' + right(run_time,2) as char (8))
	END as 'startTime',
CASE len(run_duration)
		WHEN 1 THEN cast('00:00:0'
				+ cast(run_duration as char) as char (8))
		WHEN 2 THEN cast('00:00:'
				+ cast(run_duration as char) as char (8))
		WHEN 3 THEN cast('00:0'
				+ Left(right(run_duration,3),1)
				+':' + right(run_duration,2) as char (8))
		WHEN 4 THEN cast('00:'
				+ Left(right(run_duration,4),2)
				+':' + right(run_duration,2) as char (8))
		WHEN 5 THEN cast('0'
				+ Left(right(run_duration,5),1)
				+':' + Left(right(run_duration,4),2)
				+':' + right(run_duration,2) as char (8))
		WHEN 6 THEN cast(Left(right(run_duration,6),2)
				+':' + Left(right(run_duration,4),2)
				+':' + right(run_duration,2) as char (8))
	END as 'duration' from msdb..sysjobs sj inner 
join sysjobhistory sjh on sj.job_id=sjh.job_id
where sjh.step_id = 0 and sjh.run_date >= '%s' and sj.name not in ('syspolicy_purge_history', 'RefreshADGroupInfo')
order by runDate, startTime, jobName, duration
""" % yesterday

for server in serverList:
	cn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=msdb;Trusted_Connection=yes' % server.strip())
	cursor = cn.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	toAddrs = ['myEmail@myCompany.com']
	subj = '%s job status since yesterday' % server.strip()
	msg = """\
%s
""" % cursorResultsPrettyPrint(cursor, rows, True)

	sendEmail(toAddrs, subj, msg)
