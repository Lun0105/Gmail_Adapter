# Gmail_Adapter
This is a Gmail Assistant Package, which helps you fetching informations from target Gmail.

**Class Mail** contains basic information of a single email  
- [Mail(ID:str, raw_data:str)](#Class_Mail)  
  - details()
  - download_attachment(path:str, coding_style="utf-8")

**Class Gmail** contains basic information of your email account  
- [Gmail(email_address:str, token='token.json', reAuth=False)](#Class_Gmail)  
  - extendMailbox(num=1)
  - Print(amount=10)
  - FindById(ID:str)
  - FindByTittle(tittle:str, limit=10)
  - FindByKeyword(keyword:str, consistance=True, limit=10)
  - FindBySender(sender:str, limit=10)
  - sortLabel(emailId:str, name:str, add=True)
  - sent_mes(To:str, Subject:str, context:str, file=None)

## Class_Mail:
- `self.id` this mail's id
- `self.message` main resources(type:email.message.Message)
- `self.head` header
- `self.sender` sender
- `self.reciever` receiver
- `self.date` send date
  
**_ _init_ _(ID:str, raw_data:str)->None:**  
translate rawdata (type:RFC 2822) to readable self.message (type:email.message.Message)  
`Args` Id=id of the mail, raw_data=raw dataof a single e-mail
`return` None

**details()->None:**  
print header, sender, receiver, send date  
`Args` None  
`return` None

**download_attachment(path:str, coding_style="utf-8")->None:**
download the attachment if exist  
`Args` path=where you save the attachment, coding_style=the way to decode the file
`return` None

## Class_Gmail:
- `self.mailbox` mails included 'id', 'labelIds'
- `self.capacity` size of fetched mails in your mailbox
- `self.Labels` Labels in your gmail

**_ _init_ _(email_address:str, token='token.json', reAuth=False)->None:**  
send a request to access the information of the Gmail account  
`Args` email_address=the email addresss to be accessed, token=the path to the auth token, reAuth=a bool determined if reauthorize the account  
`return` None

**extendMailbox(num=1)->None**
the default amount of mails in initial request is 500, this function extend (500 * num) mails
`Args` num=times 500 mails to be added
`return` None

**Print(amount=10)->None**
output details of mials in mailbox
`Args` amount=amount of mails to be printed
`return` None

**FindById(ID:str)->Mail**
output details of mials in mailbox
`Args` amount=amount of mails to be printed
`return` None

**FindByTittle(tittle:str, limit=10)->Mail**

**FindByKeyword(keyword:str, consistance=True, limit=10)->List**

**FindBySender(sender:str, limit=10)->List**

**sortLabel(emailId:str, name:str, add=True)->None**

**sent_mes(self, To:str, Subject:str, context:str, file=None)->None**
