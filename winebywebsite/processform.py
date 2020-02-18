import cgi, cgitb
formData = cgi.FieldStorage()

firstName = formData.getvalue('fname')
lastName = formData.getvalue('lname')
email = formData.getvalue('email')
store = formData.getvalue('store')
#ageConf = formData.getvalue('age')


print("Content-type:text/html")

#print """ Content-type text/html\n\n
#	<!DOCTYPE html>
#	<html lang="en"
#		<head>
#			<title>Server-sized scripting</title>
#		</head>
#		<body>
#			<p> In the first name box you entered {0} </p>
#			<p> in the email box you entered {1} </p>
#		</body>
#	</html>
#""" .format(firstName, email)



print
print("")
print("")
print("Hello - Second CGI Program")
print("")
print("")
print("
   Hello %s %s
   " % (firstName, lastName))
print("")
print("")