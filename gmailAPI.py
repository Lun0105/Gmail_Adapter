import base64
import email.header
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

class Mail:
    @staticmethod
    def decode_raw_mes(raw_data:str)->str:
        message = email.message_from_bytes(base64.urlsafe_b64decode(raw_data))
        return message

    @staticmethod
    def decode_mes_ele(mes:str)->str:
        mes = email.header.make_header(email.header.decode_header(mes))
        decoded_raw = str(mes)
        return decoded_raw  
    
    def __init__(self, raw_data:str) -> None:
        self.elements = ['Subject', 'From', 'To', 'Date']
        self.message =  self.decode_raw_mes(raw_data)
        self.head = self.decode_mes_ele(self.message[self.elements[0]])
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

class Gmail:
    def __init__(self, email_address:str, token='token.json')->None:
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.__email_address = email_address
        self.__token = token
        self.__creds = Credentials.from_authorized_user_file(self.__token, SCOPES)
        self.__service = build('gmail', 'v1', credentials=self.__creds)
        results = self.__service.users().messages().list(userId=self.__email_address).execute()
        self.mailbox = results['messages'] #{'id':*, 'labelIds':*}
        return
    
    def Print(self, amount=10)->None:
        i = 0
        for mail in self.mailbox:
            spc = self.getById(mail['id'])
            spc.details()
            print()
            i+=1
            if (i == amount):break;
        return
    
    def getById(self, ID:str)->Mail:
        res = self.__service.users().messages().get(userId=self.__email_address, id = ID, format='raw').execute()
        mail = Mail(res['raw'])
        return mail
    
    def FindByTittle(self, tittle:str, Range=10)->Mail:
        try:    
            count = 0
            for mail in self.mailbox:
                count += 1
                ID = mail['id']
                res = self.__service.users().messages().get(userId=self.__email_address, id = ID, format='raw').execute()
                this_mail = Mail(res['raw'])
                if this_mail.head == tittle:
                    break
                if count >= 10:
                    assert False, f"mail named [{tittle}] not found in {Range} recent mails"
            return this_mail    
        except AssertionError as msg:
            print(msg)