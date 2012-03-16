import smtplib, string, sys

def sendEmail(toAddress, subject, msg):
	fromAddress = 'fromAddress@myCompany.com'
	smtpServer = 'smtp.myCompany.com'    # Put your own email server here.
   	# toAddress MUST be a python list of email addresses.
   	# Convert list to string.
   	toAddressString = string.join(toAddress, ",")
   	# Convert msg to smtp format.
   	msg = """\
To: %s
From: %s
Subject: %s

%s
""" % (toAddressString, fromAddress, subject, msg)
   	try:
      		server = smtplib.SMTP(smtpServer)
      	# If your mail server requires a username/login, you'll need the following line.
      	#server.login('myLogin', 'myPassword')
      		server.sendmail(fromAddress, toAddress, msg)
      		server.quit()
   	except:
      		print "Error sending email. Possible SMTP server error"
      		sys.exit(1)

#Below is sample test code
#toAddress = ['person1@foo.com', 'person2@bar.com']
#subject = 'Hello there!'
#msg = """Hi yo
#Have a nice day!
#Bye.
#Sincerely yours
#"""
#sendEmail(toAddress, subject, msg)
