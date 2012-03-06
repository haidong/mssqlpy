import re, shlex, subprocess, sys
from datetime import datetime
"""Haidong's class of Windows-specific utilities. It uses sysinternal tools fairly extensively. This is written mostly for SQL Server administration"""
def runCmd(cmd):
	proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = proc.communicate()
	ret = proc.returncode
	return (ret, out, err)

def getServiceStartupAccount(serviceName, serverName):
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % serviceName, re.IGNORECASE)
	startupAccount = re.compile(r'\tSERVICE_START_NAME:\s(.+)')

	returnCode, stdOut, stdErr = runCmd("""psservice \\\\%s config""" % serverName.strip())
	targetServiceFound = False

	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = startupAccount.search(line)
			if reResult:
				return reResult.group(1)
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
	
	if not targetServiceFound:
		return None
