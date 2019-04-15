from urllib.request import urlopen
import json 
token = '731472091:AAGGqOJK_HEmYxpuHwMKwyZw25rJ9bLIThU'
api_url = "https://api.telegram.org/bot"
api_url2 = "https://www.notifymydevice.com/push?ApiKey=FY9YJ498F5ZTNGEVVTX6MJB6C&PushTitle=Washroom%20Maintainance%20&PushText=Kindly%20take%20a%20look%20into%20washroom,%20it%20seems%20it%20is%20not%20in%20usable%20condition"

def sendMessage(text,chat_id):
    query = api_url+token+"/sendMessage?chat_id="+chat_id+"&text="+text
    Client = urlopen(query)
    page=Client.read()
    page = str(page)
    Client.close()
    #json_page = json.loads(page)

def sendnmd():
    Client = urlopen(api_url2)
    page=Client.read()
    page = str(page)
    Client.close()
    return "sent!"
 
