# Gmail_Adapter
This is a Gmail Assistant Package, which helps you fetching informations from target Gmail.

**Class Mail** contains basic information of a single email  
- [Mail(self, raw_data:str)](#Class_Mail)
  - decode_raw_mes(raw_data:str)
  - decode_mes_ele(mes:str)
  - details(self)
  - download_attachment(self, path:str, coding_style="utf-8")
  - decode_context(self)

**Class Gmail** contains basic information of your email account

## Class_Mail:
**Public:**
- `self.message` main resources(type:email.message.Message)
- `self.head` header
- `self.sender` sender
- `self.reciever` receiver
- `self.date` send date

#### **decode_raw_mes(raw_data:str)->str:**  
you won't be using this fuction

#### **decode_mes_ele(mes:str)->str:**  
you won't be using this fuction

**_ _init_ _(self, raw_data:str) -> None:**  
translate rawdata (type:RFC 2822) to readable self.message (type:email.message.Message)  
`Args` raw data of a single e-mail  
`return` None

**details(self)->None:**  
printing header, sender, receiver, send date  
`Args` None  
`return` None

**download_attachment(self, path:str, coding_style="utf-8")->None:**
    
**decode_context(self)->str:**
