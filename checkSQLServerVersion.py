import argparse
from mssqlUtility import getVersionNumber
from allPlatUtility import sendEmail

parser = argparse.ArgumentParser(description='Check SQL Server version number')
parser.add_argument('-f', '--fileInput', help='The presence of this parameter indicates server names come from a file',  action='store_true', default=False, dest='fileInput')
parser.add_argument('-i', '--input', help='When -f is present, please provide the name of the file that contains a list of servers, each on its own line. Otherwise, please type a list of servers, separated by comma.',  required=True, dest='iInput')

argList = parser.parse_args()
standardVersion = '10.50.2789.0'

emailMsg = ''
if argList.fileInput:
	text_file = open("%s" % argList.iInput, "r")
	serverList = text_file.readlines()
else:
	serverList = argList.iInput.split(',')

for server in serverList:
	version = getVersionNumber(server.strip())
	if version != standardVersion:
		if version is None:
			emailMsg = emailMsg + server.strip() + ' is down or does not exist\n'
		else:
			emailMsg = emailMsg + server.strip() + ' is version ' + version + ' not ' + standardVersion + ', which is our standard\n'

if emailMsg != '':
	toAddress = ['myEmail@myCompany.com']
	subject = 'Server connectivity and version test'
	sendEmail(toAddress, subject, emailMsg)
