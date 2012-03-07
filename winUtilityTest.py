import unittest
import winUtility

class winUtilityTest(unittest.TestCase):
	def test_runCmd_dir_stdErr(self):
		returnCode, stdOut, stdErr = winUtility.runCmd("dir")
		self.assertEqual(stdErr, '')
	def test_runCmd_dir_stdOut(self):
		returnCode, stdOut, stdErr = winUtility.runCmd("dir")
		self.assertIn("winUtility.py", stdOut)
	def test_getServiceStartupAccount_dhcp(self):
		self.assertEqual(winUtility.getServiceStartupAccount('Dhcp', 'LocalHost'), 'NT Authority\\LocalService')
