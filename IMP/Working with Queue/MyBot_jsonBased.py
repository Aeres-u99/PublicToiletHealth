import time 
import botogram
import pickle
import Module.poop as p


chat_id_group = "-1001417234342"


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
        "Usage Count":"",
        "Water Level":""
                }
primary_gasbuffer = []
primary_ldrbuffer = []
primary_pc = []
primary_wl = []

def ModVar():
    gas_object = open("file_gas",'rb')
    ldr_object = open("file_ldr",'rb')
    pc_object = open("file_pc", 'rb')
    wl_object = open("file_wl",'rb')
    primary_gasbuffer = pickle.load(gas_object)
    primary_ldrbuffer = pickle.load(ldr_object)
    primary_pc = pickle.load(pc_object)
    primary_wl = pickle.load(wl_object)
    primary_sent["Gas Sensor"] = primary_gasbuffer[-1]
    primary_sent["LDRSensor"] = primary_ldrbuffer[-1]
    primary_sent["Usage Count"] = primary_pc[-1]
    primary_sent["Water Level"] = primary_wl[-1]
    gas_object.close()
    ldr_object.close()
    pc_object.close()
    wl_object.close()
    print(primary_sent)

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
    wl_object = open("file_wl",'rb')
    primary_gasbuffer = pickle.load(gas_object)
    primary_ldrbuffer = pickle.load(ldr_object)
    primary_pc = pickle.load(pc_object)
    primary_wl = pickle.load(wl_object)
    primary_sent["Gas Sensor"] = primary_gasbuffer[-1]
    primary_sent["LDRSensor"] = primary_ldrbuffer[-1]
    primary_sent["Usage Count"] = primary_pc[-1]
    primary_sent["Water Level"] = primary_wl[-1]
    print(primary_gasbuffer)
    print(primary_ldrbuffer)
    print(primary_pc)
    print(primary_wl)
    gas_object.close()
    ldr_object.close()
    pc_object.close()
    wl_object.close()
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

@bot.command("getWaterLevel")
def getWaterLevel(chat,message):
    """Water Level in washroom tank"""
    wl_object = open("file_wl",'rb')
    primary_wl = pickle.load(wl_object)
    primary_sent["Water Level"] = primary_wl[-1]
    wl_object.close()
    chat.send(str(primary_sent["Water Level"]))

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

@bot.command("val_WlAll")
def val_wlAll_command(chat,message,args):
    """Entire WL Buffer, might be more than 4096 chars."""
    wl_object = open("file_wl",'rb')
    primary_wl = pickle.load(wl_object)
    wl_object.close()    
    btns = botogram.Buttons()
    btns[0].callback("Delete this message","delete")
    chat.send(str(primary_ldrbuffer), attach=btns)



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

def checkCondition(valWL,valGas,valLDR,valPC):
    valPC = float(valPC)
    valWL = float(valWL)
    valGas = float(valGas)
    valLDR = float(valLDR)

    if (valWL < 20 and valGas < 40 and valLDR > 700):
        NotifMessage = """ Washroom is becoming unusable, please check the Conditions.
                           Water level is low, Gas is clean and There is not sufficient luminosity.
                           Suggestions: 
                                        1). Check water Supply.
                                        3). Check the Bulbs.
                        """

        SendNotifications(NotifMessage);
        return 1

    elif (valWL < 20 and valGas > 70 and ( (valLDR > 400) and (valLDR < 700) )):
        NotifMessage = """ Washroom is becoming unusable, please check the Conditions.
                           Water level is low, Gas is Unclean and There is sufficient luminosity.
                           Suggestions: 
                                        1). Check water Supply.
                                        2). Check Whether the washroom is flushed
                                    
                        """
 
        SendNotifications(NotifMessage);
        return 2
    elif (((valWL < 60) and (valWL > 20)) and valGas > 70 and (valLDR > 700) ):
        NotifMessage = """ Washroom is becoming unusable, please check the Conditions.
                           Water level is Average, Gas is Unclean and There is not sufficient luminosity.
                           Suggestions: 
                                        1). Check water Supply.
                                        2). Check Whether the washroom is flushed
                                        3). Replace the broken bulbs if any.
                                    
                        """
 
        SendNotifications(NotifMessage);
        return 3
    elif (valWL < 20 and valGas > 70 and (valLDR > 700) ):
        NotifMessage = """ Washroom is becoming unusable, please check the Conditions.
                           Water level is low, Gas is Unclean and There is not sufficient luminosity.
                           Suggestions: 
                                        1). Check water Supply.
                                        2). Check Whether the washroom is flushed.
                                        3). Check whether bulb is proper or not.
                                    
                        """
 
        SendNotifications(NotifMessage);
        return 4
    elif (valWL < 20 and valGas > 40 and ((valLDR < 300))):
        NotifMessage = """ Washroom is becoming unusable, please check the Conditions.
                           Water level is low, Gas is Moderately clean and There is More than enough luminosity.
                           Suggestions: 
                                        1). Check water Supply.
                                        2). Check Whether the washroom is flushed
                                  
                                    
                        """
 
        SendNotifications(NotifMessage);
        return 5
    elif (valWL > 20 and valWL < 60 and valGas > 70 and ( (valLDR > 300) and (valLDR < 400) )):
        NotifMessage = """ Washroom is becoming unusable, please check the Conditions.
                           Water level is Average, Gas is Unclean and There is Moderate luminosity.
                           Suggestions: 
                                    
                                        2). Check Whether the washroom is flushed
                                    
                        """
 
        SendNotifications(NotifMessage);
        return 6
    elif (valWL < 20 and valGas > 70 and ( (valLDR > 300) and (valLDR < 700) )):
        NotifMessage = """ Washroom is becoming unusable, please check the Conditions.
                           Water level is low, Gas is Unclean and There is sufficient luminosity.
                           Suggestions: 
                                        1). Check water Supply.
                                        2). Check Whether the washroom is flushed
                                    
                        """
        SendNotifications(NotifMessage);
        return 7

    elif(valPC > 150):
        NotifMessage = """ Washroom has been used a lot, please look into it for once """
        SendNotifications(NotifMessage)
        return 8
    
    else:
        print(" Nothing serious ^_^ ")
        return "k"

 
 


def SendNotifications(notifMessage):
    """Sends the Notifications""" 
    p.sendMessage(notifMessage,chat_id_group)




if __name__ == "__main__":
    while(1):
        checkCondition(1,2,3,4);
        SendNotifications("Bot has been Initiated.")   
        bot.run()
