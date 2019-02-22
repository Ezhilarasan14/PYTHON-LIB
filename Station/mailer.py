# Python code to illustrate Sending mail from  
# your Gmail account  
import smtplib 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("nec0914014@gmail.com", 89026180) 
  
# message to be sent 
message = "Message_you_need_to_send"
  
# sending the mail 
s.sendmail("nec0914014@gmail.com", "ezhil@tocode.tech", message) 
  
# terminating the session 
s.quit() 
