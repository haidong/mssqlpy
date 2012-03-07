import re, shlex, subprocess, sys
from datetime import datetime
"""Haidong's class of Windows-specific utilities. It uses sysinternal tools fairly extensively. This is written mostly for SQL Server administration"""
def runCmd(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = proc.communicate()
	ret = proc.returncode
	return (ret, out, err)

def getServiceStartupAccount(service, serverName):
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % service, re.IGNORECASE)
	startupAccount = re.compile(r'\tSERVICE_START_NAME:\s(.+)')

	cmd = """psservice \\\\%s config""" % serverName.strip()
	returnCode, stdOut, stdErr = runCmd(cmd)
	targetServiceFound = False

	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = startupAccount.search(line)
			if reResult:
				return reResult.group(1).strip()
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
	
	if not targetServiceFound:
		return None
