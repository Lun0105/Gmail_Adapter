import base64
import email.header
import os
import mimetypes
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from email.message import EmailMessage
from email.utils import format_datetime
from datetime import datetime

class Mail:
    @staticmethod
    def decode_raw_mes(raw_data:str)->str:
        if raw_data == None:
            return "None"
        message = email.message_from_bytes(base64.urlsafe_b64decode(raw_data))
        return message

    @staticmethod
    def decode_mes_ele(mes:str)->str:
        if mes == None:
            return "None"
        mes = email.header.make_header(email.header.decode_header(mes))
        decoded_raw = str(mes)
        return decoded_raw  
    
    def __init__(self, ID:str, raw_data:str) -> None:
        self.id = ID
        self.elements = ['Subject', 'From', 'To', 'Date']
        self.message =  self.decode_raw_mes(raw_data)
        self.head = self.decode_mes_ele(self.message[self.elements[0]])
        self.body = self.decode_context()
        self.sender = self.decode_mes_ele(self.message[self.elements[1]])
        self.reciever = self.decode_mes_ele(self.message[self.elements[2]])
        self.date = self.message[self.elements[3]]
        return

    def details(self)->None:
        print("header : ",self.head)
        print("From : ",self.sender)
        print("To : ",self.reciever)
        print("Date : ",self.date)
        print("text : ", self.body[0:20])
        return 

    def download_attachment(self, path:str, coding_style="utf-8")->None:
        for part in self.message.walk():
            if part.get("Content-Disposition") is not None:
                filename = part.get_filename()
                if filename:
                    # encoding file name
                    decoded_filename = email.header.decode_header(filename)[0][0]
                    if decoded_filename:
                        if isinstance(decoded_filename, bytes):
                            # decode the file with correspond coding style
                            decoded_filename = decoded_filename.decode(coding_style)
                        # assigning downloading path
                        download_dir = path
                        # building complete path
                        file_path = os.path.join(download_dir, decoded_filename)
                        # saving the flie to direct path
                        with open(file_path, "wb") as f:
                            f.write(part.get_payload(decode=True))
                        print(f"dowlaoding_file: {decoded_filename}")
        return 
    
    def decode_context(self)->str:
        body = ""
        if self.message.is_multipart():
            for part in self.message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "text/plain" in content_type and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', 'ignore')#'latin-1', 'replace')
        else:body = self.message.get_payload(decode=True).decode();
        return body

class Gmail:
    def __init__(self, email_address:str, token='token.json', reAuth=False)->None:
        SCOPES = ["https://www.googleapis.com/auth/gmail.modify","https://www.googleapis.com/auth/gmail.labels"]
        self.__email_address = email_address
        creds = None  
        if reAuth:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        else:
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file(token, SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and not creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
        self.__service = build('gmail', 'v1', credentials=creds)
        results = self.__service.users().messages().list(userId=self.__email_address, maxResults=500).execute()
        self.mailbox = results['messages'] #{'id':*, 'labelIds':*}
        self.capacity = len(self.mailbox)
        self.next_page_token = results.get('nextPageToken')
        res_lebel = self.__service.users().labels().list(userId="me").execute()
        labels = res_lebel.get("labels", [])
        self.lables = labels
        return

    def extendMailbox(self, num=1)->None:
        while num and self.next_page_token:
            results = self.__service.users().messages().list(userId=self.__email_address, maxResults=500, pageToken=self.next_page_token).execute()
            self.mailbox += results['messages'] #{'id':*, 'labelIds':*} 
            self.next_page_token = results.get('nextPageToken')
            self.capacity = len(self.mailbox)
            num -= 1
        return

    def Print(self, amount=10)->None:
        i = 0
        for mail in self.mailbox:
            spc = self.FindById(mail['id'])
            spc.details()
            print()
            i+=1
            if i == amount:break;
        return
    
    def FindById(self, ID:str)->Mail:
        res = self.__service.users().messages().get(userId=self.__email_address, id = ID, format='raw').execute()
        mail = Mail(ID, res['raw'])
        return mail
    
    def FindByTittle(self, tittle:str, limit=10)->Mail:
        try:   
            turn = 0
            for mail in self.mailbox:
                turn += 1
                ID = mail['id']
                res = self.__service.users().messages().get(userId=self.__email_address, id = ID, format='raw').execute()
                this_mail = Mail(ID, res['raw'])
                if this_mail.head == tittle:
                    break
                if turn >= limit:
                    assert False, f"mail named [ {tittle} ] not found in {limit} recent mails"
            return this_mail    
        except AssertionError as msg:
            print(msg)

    def FindByKeyword(self, keyword:str, consistance=True, limit=10)->list:
        try:    
            turn = 0
            find = False
            result =[]
            for mail in self.mailbox:
                turn += 1
                ID = mail['id']
                res = self.__service.users().messages().get(userId=self.__email_address, id = ID, format='raw').execute()
                this_mail = Mail(ID, res['raw'])
                if consistance:
                    if keyword in this_mail.head:
                        find=True
                        result.append(this_mail)
                else:
                    for keys in this_mail.head:
                        if keys in keyword:
                            find=True
                            result.append(this_mail)
                            break
                if turn >= limit:
                    if find:break;
                    assert False, f"header includes [ {keyword} ] not found in {limit} recent mails"
            return result
        except AssertionError as msg:
            print(msg)
    
    def FindBySender(self, sender:str, limit=10)->list:
        try:    
            turn = 0
            result = []
            find = False
            for mail in self.mailbox:
                turn += 1
                ID = mail['id']
                res = self.__service.users().messages().get(userId=self.__email_address, id = ID, format='raw').execute()
                this_mail = Mail(ID, res['raw'])
                if sender in this_mail.sender:
                    find=True
                    result.append(this_mail)
                if turn >= limit:
                    if find:break;
                    assert False, f"mail sended by {sender} not found in {limit} recent mails";
            return result    
        except AssertionError as msg:
            print(msg)
    
    def sortLabel(self, emailId:str, name:str, add=True)->None:
        found = False
        labelID = None
        for label in self.lables:
            if label["name"] == name:
                found = True
                labelID = label["id"]
        if not found:
            self.__service.users().labels().create(userId="me",body={"name":name}).execute()
            res_lebel = self.__service.users().labels().list(userId="me").execute()
            labels = res_lebel.get("labels", [])
            self.lables = labels
            for label in self.lables:
                if label["name"] == name:labelID = label["id"];
        if add:
            self.__service.users().messages().modify(userId=self.__email_address, id=emailId, body={'addLabelIds':[labelID]}).execute()
        else:
            self.__service.users().messages().modify(userId=self.__email_address, id=emailId, body={'removeLabelIds':[labelID]}).execute()
        return

    def sent_mes(self, To:str, Subject:str, context:str, file=None)->None:
        message = EmailMessage()
        message.set_content(context)
        message["To"] = To
        #message["From"] = From
        message["Subject"] = Subject
        if file:
            # guessing the MIME type
            type_subtype, _ = mimetypes.guess_type(file)
            maintype, subtype = type_subtype.split("/")
            with open(file, "rb") as fp:
                attachment_data = fp.read()
            message.add_attachment(attachment_data, maintype, subtype, filename= file)
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (self.__service.users().messages().send(userId="me", body=create_message).execute())
        print(f'Message Id: {send_message["id"]}')
        return
