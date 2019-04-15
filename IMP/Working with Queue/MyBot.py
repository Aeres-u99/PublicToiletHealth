import Buffer_operation as bo 
import botogram
import pickle

bot = botogram.create("731472091:AAGGqOJK_HEmYxpuHwMKwyZw25rJ9bLIThU")
bot.about = '''This is a bot created for Sending the values from Sensors and to detect whether the washroom is clean or not'''

bot.owner = '''@KuroAkuma'''

bot.after_help =  [
        """This bot is capable of fetching the realtime data with command /getData, more features will be coming in future. Feel free to ping Aeres on Freenode irc servers, [not on bouncer anymore tho, if not found worry not]. mostly hangs around in #anime, ##anime. @KuroAkuma is the telegram[keeps changing and hard to track]. 
        Mail: aeres99@hotmail.com [replies within a week!]
        """]

primary_sent = {
        "Gas Sensor":"",
        "LDRSensor":"",
        "Usage Count":""
                }
primary_gasbuffer = []
primary_ldrbuffer = []
primary_pc = []


@bot.command("greetMe")
def greetMe_command(chat,message,args):
    """Says hello world to the person whose name is provided"""
    test_str="Konichiwa" 
    test_str_2="Senpai, watashi Anata no jujun'na shimo be"
    if len(args)>0:
        test_str+= " "+args[0]
        test_str+=test_str_2
    else:
        test_str+=" "+test_str_2;
    chat.send(test_str)

@bot.command("github_Akuma")
def github_link_command(chat,message):
    """send Akuma's github profile"""
    chat.send("https://github.com/Aeres-u99")

@bot.command("getData")
def getData_command(chat,message):
    """Latest gas Sensor and LDR sensor value"""
    gas_object = open("file_gas",'rb')
    ldr_object = open("file_ldr",'rb')
    pc_object = open("file_pc", 'rb')
    primary_gasbuffer = pickle.load(gas_object)
    primary_ldrbuffer = pickle.load(ldr_object)
    primary_pc = pickle.load(pc_object)
    primary_sent["Gas Sensor"] = primary_gasbuffer[-1]
    primary_sent["LDRSensor"] = primary_ldrbuffer[-1]
    primary_sent["Usage Count"] = primary_pc[-1]
    gas_object.close()
    ldr_object.close()
    chat.send(str(primary_sent))

@bot.command("getGasSensorValue")
def getGasSensorVal_command(chat,message):
    """Latest Gas sensor value"""
    gas_object = open("file_gas",'rb')
    primary_gasbuffer = pickle.load(gas_object)
    primary_sent["Gas Sensor"] = primary_gasbuffer[-1]
    gas_object.close()
    chat.send(str(primary_sent["Gas Sensor"]))
    
@bot.command("getLDRVal")
def LDRVal_command(chat,message):
    """ Latest LDR sensor value"""
    ldr_object = open("file_ldr",'rb')
    primary_ldrbuffer = pickle.load(ldr_object)
    primary_sent["LDRSensor"] = primary_ldrbuffer[-1]
    ldr_object.close()
    chat.send(str(primary_sent["LDRSensor"]))

@bot.command("getUsageCount")
def getUsageCount_command(chat,message):
    """Entire washroom usage count"""
    pc_object = open("file_pc",'rb')
    primary_pc = pickle.load(pc_object)
    primary_sent["Usage Count"] = primary_pc[-1]
    pc_object.close()
    chat.send(str(primary_sent["Usage Count"]))

@bot.command("val_gasAll")
def gasAll_command(chat,message,args):
    """Entire gas buffer, might be more than 4096chars."""
    gas_object = open("file_gas",'rb')
    ldr_object = open("file_ldr",'rb')
    primary_gasbuffer = pickle.load(gas_object)
    primary_ldrbuffer = pickle.load(ldr_object)
    gas_object.close()
    ldr_object.close()
    btns = botogram.Buttons()
    btns[0].callback("Delete this message","delete")
    chat.send(str(primary_gasbuffer), attach=btns)

@bot.command("val_LDRAll")
def val_ldrAll_command(chat,message,args):
    """Entire LDR Buffer, might be more than 4096 chars."""
    gas_object = open("file_gas",'rb')
    ldr_object = open("file_ldr",'rb')
    primary_gasbuffer = pickle.load(gas_object)
    primary_ldrbuffer = pickle.load(ldr_object)
    gas_object.close()
    ldr_object.close()
    btns = botogram.Buttons()
    btns[0].callback("Delete this message","delete")
    chat.send(str(primary_ldrbuffer), attach=btns)

@bot.callback("delete")
def delete_callback(query,chat,message):
    message.delete()
    query.notify("Message deleted!")

if __name__ == "__main__":
        bot.run()
