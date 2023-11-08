import base64
import email.header
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

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
    
    def __init__(self, raw_data:str) -> None:
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
                    body = part.get_payload(decode=True).decode()
        else:body = self.message.get_payload();
        return body

class Gmail:
    def __init__(self, email_address:str, token='token.json')->None:
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.__email_address = email_address
        self.__creds = Credentials.from_authorized_user_file(token, SCOPES)#None
        if os.path.exists('token.json'):
            self.__creds = Credentials.from_authorized_user_file(token, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.__creds.to_json())
        self.__service = build('gmail', 'v1', credentials=self.__creds)
        results = self.__service.users().messages().list(userId=self.__email_address, maxResults=50).execute()
        self.mailbox = results['messages'] #{'id':*, 'labelIds':*}
        return
    
    def extendMailbox(self, num=50)->None:
        results = self.__service.users().messages().list(userId=self.__email_address, maxResults=50+num).execute()
        self.mailbox = results['messages'] #{'id':*, 'labelIds':*}
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
        mail = Mail(res['raw'])
        return mail
    
    def FindByTittle(self, tittle:str, limit=10)->Mail:
        try:   
            turn = 0
            for mail in self.mailbox:
                turn += 1
                ID = mail['id']
                res = self.__service.users().messages().get(userId=self.__email_address, id = ID, format='raw').execute()
                this_mail = Mail(res['raw'])
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
                this_mail = Mail(res['raw'])
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
                this_mail = Mail(res['raw'])
                if sender in this_mail.sender:
                    find=True
                    result.append(this_mail)
                if turn >= limit:
                    if find:break;
                    assert False, f"mail sended by {sender} not found in {limit} recent mails";
            return result    
        except AssertionError as msg:
            print(msg)
    
    def sortLabel(self, label:str, idList:list)->None:
        return

    def sent_mes(self, target:str)->None:
        return
