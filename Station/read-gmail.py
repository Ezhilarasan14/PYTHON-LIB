import os
import poplib
import string, random
import plone.rfc822 as rfc822
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import logging
from email.parser import Parser

class Gmail:
    def __init__(self):
        self.isConnection = False
        self.server_name= "pop.gmail.com"
        self.user_name  = "*************"
        self.pass_word = "***********"
        self.port_no = '995'
        self.server = None
    
    def getConnection(self):
        logging.debug('connecting to ' + self.server_name)
        server = poplib.POP3_SSL(self.server_name,self.port_no)
        server.user(self.user_name)
        server.pass_(self.pass_word)
        self.server = server
    
    def showInfo(self):
        messageCount, totalMessageSize = self.server.stat()
        print('Email message numbers : ' + str(messageCount))
        print('Total message size : ' + str(totalMessageSize) + ' bytes.')

    def parse_email_header(self,msg):
        # just parse from, to, subject header value.
        header_list = ('From', 'To', 'Subject','Date','Received')
        
        # loop in the header list
        for header in header_list:
            # get each header value.
            header_value = msg.get(header, '')
            print(header + ' : ' + header_value)    

    def parse_email_content(self,msg):
        # get message content type.
        content_type = msg.get_content_type().lower()
        
        print('---------------------------------' + content_type + '------------------------------------------')
        # if the message part is text part.
        if content_type=='text/plain' or content_type=='text/html':
            # get text content.
            content = msg.get_payload(decode=True)
            # get text charset.
            charset = msg.get_charset()
            # if can not get charset. 
            if charset is None:
                # get message 'Content-Type' header value.
                content_type = msg.get('Content-Type', '').lower()
                # parse the charset value from 'Content-Type' header value.
                pos = content_type.find('charset=')
                if pos >= 0:
                    charset = content_type[pos + 8:].strip()
                    pos = charset.find(';')
                    if pos>=0:
                        charset = charset[0:pos]           
            if charset:
                try:
                    content = content.decode(charset)
                    
                except:
                    print("ERROR")
           
        # if this message part is still multipart such as 'multipart/mixed','multipart/alternative','multipart/related'
        elif content_type.startswith('multipart'):
            # get multiple part list.
            body_msg_list = msg.get_payload()
            # loop in the multiple part list.
            for body_msg in body_msg_list:
                # parse each message part.
                self.parse_email_content(body_msg)
        # if this message part is an attachment part that means it is a attached file.        
        elif content_type.startswith('image') or content_type.startswith('application'):
            # get message header 'Content-Disposition''s value and parse out attached file name.
            attach_file_info_string = msg.get('Content-Disposition')
            prefix = 'filename="'

            if attach_file_info_string == 'INLINE':
                prefix_inline = 'name="'
                attach_file_info = (msg.get('Content-Type'))
                pos = attach_file_info.find(prefix_inline)
                attach_file_name = attach_file_info[pos + len(prefix_inline): len(attach_file_info) - 1]
            else:
                pos = attach_file_info_string.find(prefix)
                attach_file_name = attach_file_info_string[pos + len(prefix): len(attach_file_info_string) - 1]
            
            # get attached file content.
            attach_file_data = msg.get_payload(decode=True)
            # get current script execution directory path. 
            current_path = os.path.dirname(os.path.abspath(__file__))
            # get the attached file full path.
            attach_file_path = current_path + '/' + attach_file_name
            # write attached file content to the file.
            try:
                with open(attach_file_path,'wb') as f:
                    f.write(attach_file_data)
            except:
                print("error 1")    
            print('attached file is saved in path ' + attach_file_path)             
        else:
            content = msg.as_string()
            #print(content)         

            
    def parse_email_body(self,msg):
        if (msg.is_multipart()):
            # get all email message parts.
            parts = msg.get_payload()
            # loop in above parts.
            for n, part in enumerate(parts):
                # get part content type.
                content_type = part.get_content_type()
                print('---------------------------Part ' + str(n) + ' content type : ' + content_type + '---------------------------------------')
                self.parse_email_content(msg)                
        else:
            self.parse_email_content(msg) 

    def parse_email_msg(self,msg):
        #print(msg)
        self.parse_email_header(msg)
        print("========END HEADER==========")
        self.parse_email_body(msg)
    
    def getEmail(self):
        logging.debug('listing emails')

        # get all user email list info from pop3 server.
        resp, items, octets = self.server.list()

        # loop in the mail list.
        for i in items:
            print(i)

        print(len(items))

        for i in range(1,len(items)):
            try:
                print(i)
                (resp_message, lines, octets) = self.server.retr(i)
                print('Server response message : ' + str(resp_message))
                print('Octets number : ' + str(octets))
                
                print("*********************LIST*********************")
                #print(lines)
                print("*********************LIST END*********************")

                try:
                    msg_content = b'\r\n'.join(lines).decode('utf-8')
                except:
                    print("ERROR")

                msg = Parser().parsestr(msg_content)
                self.parse_email_msg(msg)
            except:
                print("ERROR")

gmail = Gmail()
print("--------------")
gmail.getConnection()
print("--------------")
gmail.showInfo()
print("--------------")
gmail.getEmail()
print("--------------")