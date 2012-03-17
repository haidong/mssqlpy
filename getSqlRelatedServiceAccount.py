import argparse, re, subprocess, fileinput
from winUtility import runCmd

parser = argparse.ArgumentParser(description='Get service account. Only service  whose display name has the word sql in it will be returned')
parser.add_argument('-f', '--fileInput', help='The presence of this parameter indicates server names come from a file',  action='store_true', default=False, dest='fileInput')
parser.add_argument('-i', '--input', help='When -f is present, please provide the name of the file that contains a list of servers, each on its own line. Otherwise, please type a list of servers, separated by comma.',  required=True, dest='iInput')

argList = parser.parse_args()

if argList.fileInput:
	text_file = open("%s" % argList.iInput, "r")
	serverList = text_file.readlines()
else:
	serverList = argList.iInput.split(',')

serviceName = re.compile(r'^DISPLAY_NAME:\s(.*\bsql\b.*)$', re.IGNORECASE)
startupAccount = re.compile(r'^\tSERVICE_START_NAME:\s(.+)')

for server in serverList:
	returnCode, stdOut, stdErr = runCmd("""psservice \\\\%s config""" % server.strip())
	print server.strip()
	targetServiceFound = False
	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = startupAccount.search(line)
			if reResult:
				print 'Startup account: ', reResult.group(1), '\n'
				targetServiceFound = False
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
				print 'Service name: ', reResult.group(1)
