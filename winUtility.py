import shlex, subprocess, sys
from datetime import datetime
"""Haidong's class of Windows-specific utilities. It uses sysinternal tools fairly extensively. This is written mostly for SQL Server administration"""
def runCmd(cmd):
	proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = proc.communicate()
	ret = proc.returncode
	return (ret, out, err)
