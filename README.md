# Gmail_Adapter
This is a Gmail Assistant Package, which helps you fetching informations from target Gmail.

**Class Mail** contains basic information of a single email  
- [Mail(self, ID:str, raw_data:str)](#Class_Mail)  
  - details(self)
  - download_attachment(self, path:str, coding_style="utf-8")

**Class Gmail** contains basic information of your email account  
- [Gmail(self, email_address:str, token='token.json', reAuth=False)](#Class_Gmail)  
  - extendMailbox(self, num=1)
  - Print(self, amount=10)
  - FindById(self, ID:str)
  - FindByTittle(self, tittle:str, limit=10)
  - FindByKeyword(self, keyword:str, consistance=True, limit=10)
  - FindBySender(self, sender:str, limit=10)
  - sortLabel(self, emailId:str, name:str, add=True)
  - sent_mes(self, To:str, Subject:str, context:str, file=None)

## Class_Mail:
- `self.id` this mail's id
- `self.message` main resources(type:email.message.Message)
- `self.head` header
- `self.sender` sender
- `self.reciever` receiver
- `self.date` send date
  
**_ _init_ _(self, ID:str, raw_data:str)->None:**  
translate rawdata (type:RFC 2822) to readable self.message (type:email.message.Message)  
`Args` Id of the mail, raw data of a single e-mail
`return` None

**details(self)->None:**  
print header, sender, receiver, send date  
`Args` None  
`return` None

**download_attachment(self, path:str, coding_style="utf-8")->None:**
download the attachment if exist  
`Args` path=path to where you save the attachment  
`return` None

## Class_Gmail:
- `self.mailbox` mails included 'id', 'labelIds'
- `self.capacity` size of fetched mails in your mailbox
- `self.Labels` Labels in your gmail

**_ _init_ _(self, ID:str, raw_data:str)->None:**  

**extendMailbox(self, num=1)->None**

**Print(self, amount=10)->None**

**FindById(self, ID:str)->Mail**

**FindByTittle(self, tittle:str, limit=10)->Mail**

**FindByKeyword(self, keyword:str, consistance=True, limit=10)->List**

**FindBySender(self, sender:str, limit=10)->List**

**sortLabel(self, emailId:str, name:str, add=True)->None**

**sent_mes(self, To:str, Subject:str, context:str, file=None)->None**
