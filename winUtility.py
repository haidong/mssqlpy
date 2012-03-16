import re, subprocess
from datetime import datetime

"""Haidong's class of Windows-specific utilities. For now it can run commands and adjust Windows services."""

def runCmd(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = proc.communicate()
	ret = proc.returncode
	return (ret, out, err)

def getServiceStartupAccount(service, server):
	"""Getting service startup account by parsing results from
	psservice \\server config
	SQL Server named instance has $ in its name, which needs to be escaped during regex search. Ditto for server names with dot or space in them"""
	cmd = """psservice \\\\%s config""" % server.strip()

	returnCode, stdOut, stdErr = runCmd(cmd)
	targetServiceFound = False

	service = service.replace('$', '\$')
	service = service.replace('.', '\.')
	service = service.replace(' ', '\ ')
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % service, re.IGNORECASE)
	startupAccount = re.compile(r'\tSERVICE_START_NAME:\s(.+)')

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

def getServiceState(service, server):
	"""Getting service status by parsing results from
	psservice \\server query service
	SQL Server named instance has $ in its name, which needs to be escaped during regex search. Ditto for server names with dot or space in them
	Note that the command string is built before compiling the regex. Regex needs proper escape, but psservice query can take $ signs. I haven't tested if psservice can take space and/or dot in the query command"""
	
	cmd = """psservice \\\\%s query %s""" % (server.strip(), service)

	returnCode, stdOut, stdErr = runCmd(cmd)
	targetServiceFound = False

	service = service.replace('$', '\$')
	service = service.replace('.', '\.')
	service = service.replace(' ', '\ ')
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % service, re.IGNORECASE)
	serviceState = re.compile(r'\tSTATE\s+:\s(.+)')

	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = serviceState.search(line)
			if reResult:
				return reResult.group(1).partition('  ')[2].strip()
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
	
	if not targetServiceFound:
		return None

def setServiceStatus(service, server, action):
	"""Change service status by running
	psservice \\server [stop|start|restart] service
	"""	
	cmd = """psservice \\\\%s %s %s""" % (server.strip(), action, service)

	returnCode, stdOut, stdErr = runCmd(cmd)

	time1 = datetime.now()

	"""Note here that we check the status is changed properly within 30 seconds window. In other words we cannot check its state infinitely, so I picked the 30 seconds limit arbitrially. It may need to be adjusted"""
	while (datetime.now() - time1).seconds < 30:
		status = getServiceState(service, server)
		if action.upper() == 'STOP':
			return True
		elif (action.upper() == 'START') or (action.upper() == 'RESTART'):
			return True
		else:
			return False

def getServiceStartupType(service, server):
	"""Getting service startup type by parsing results from
	psservice \\server config
	SQL Server named instance has $ in its name, which needs to be escaped during regex search. Ditto for server names with dot or space in them"""
	cmd = """psservice \\\\%s config""" % server.strip()

	returnCode, stdOut, stdErr = runCmd(cmd)
	targetServiceFound = False

	service = service.replace('$', '\$')
	service = service.replace('.', '\.')
	service = service.replace(' ', '\ ')
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % service, re.IGNORECASE)
	startupType = re.compile(r'\tSTART_TYPE\s+:\s(.+)')

	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = startupType.search(line)
			if reResult:
				return reResult.group(1).partition('  ')[2].strip()
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
	
	if not targetServiceFound:
		return None

def setServiceStartupType(service, server, startupType):
	"""Changing service startup type by running:
	psservice \\server setconfig
	"""
	if startupType.lower() == 'manual':
		startupType = 'demand'
	elif startupType.lower() == 'automatic':
		startupType = 'auto'
	elif startupType.lower() == 'disable':
		startupType = 'disabled'

	cmd = """psservice \\\\%s setconfig %s %s""" % (server.strip(), service.strip(), startupType.strip())

	returnCode, stdOut, stdErr = runCmd(cmd)

	setResult = getServiceStartupType(service, server)

	if startupType == 'demand':
		if setResult == 'DEMAND_START':
			return True
	elif startupType == 'auto':
		if setResult == 'AUTO_START (DELAYED)':
			return True
	elif startupType == 'disabled':
		if setResult == 'DISABLED':
			return True
	
	return False
