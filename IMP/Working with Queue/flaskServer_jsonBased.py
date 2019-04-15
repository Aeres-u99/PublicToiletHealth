import flask 
from flask import request,jsonify,render_template
import Module.poop as p
import pickle
import json
chat_id_group = "-1001417234342"

# buffer variables
# are meant to be declared here, we will share the stuffs 
# with botogram bot!


data = {
        "LDR Value":"",
        "Person Counter":"",
        "Gas Sensor":"",
        "Water Level":""
        }

primary_Gasbuffer = []
primary_LDRbuffer = []
usageCounter = []
waterLevel = []


#Std query format /update?valGas=100.00&valLDR=1015" 404 -

app = flask.Flask(__name__)
app.config["DEBUG"] = True 

@app.route('/',methods = ['GET'])
def home_main():
    return "<h1>Yaaay! this is basic website, it literally does nothing</h1>"

@app.route('/update',methods=['GET'])
def Call_message():
    if 'valGas' in request.args:
        valGas = request.args['valGas']
        if 'valLDR' in request.args:
            valLDR = request.args['valLDR']
            if 'valPC' in request.args:
                valPC = request.args['valPC']
                if 'valWL' in request.args:
                    valWL = request.args['valWL']
                    
                    data["LDR Value"] = valLDR
                    data["Person Counter"] = valPC
                    data["Gas Sensor"] = valGas
                    data["Water Level"] = valWL
                    print(valGas+" "+valLDR+" "+valPC+" "+valWL)
                    primary_Gasbuffer.append(valGas)
                    primary_LDRbuffer.append(valLDR)
                    usageCounter.append(valPC)
                    waterLevel.append(valWL)

                    wlBuffer = "file_wl"
                    wl_object = open(wlBuffer, 'wb')
                    gasBuffer = "file_gas"
                    gas_object = open(gasBuffer, 'wb')
                    ldrBuffer = "file_ldr"
                    ldr_object = open(ldrBuffer, 'wb')
                    pcBuffer = "file_pc"
                    pc_object = open(pcBuffer, 'wb')
                    #Stuffs ^ 
                    checkCondition(valWL,valGas,valLDR,valPC)
                    
                    pickle.dump(primary_Gasbuffer,gas_object)
                    pickle.dump(primary_LDRbuffer,ldr_object)
                    pickle.dump(usageCounter,pc_object)
                    pickle.dump(waterLevel,wl_object)

                    gas_object.close()
                    ldr_object.close()
                    pc_object.close()
                    
                    with open('json_dump.json','a') as f:
                        f.write("\n");
                        json.dump(data,f)
                
                
                    
                    return ""
    else:
            return " "
    
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


def checkCondition(valWL,valGas,valLDR,valPC):
    valPC = float(valPC)
    valWL = float(valWL)
    valGas = float(valGas)
    valLDR = float(valLDR)
    print("ldr: ",valLDR)
    print("water level: ",valWL)
    print("gas value: ",valGas)
    print("person count:",valPC)

    if (valWL < 20 and valGas < 40 and valLDR > 700):
        NotifMessage = "Washroom is becoming unusable, please check the Conditions.Water level is low, Gas is clean and There is not sufficient luminosity.Suggestions:1). Check water Supply. 3). Check the Bulbs."
        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC)            
        SendNotifications(NotifMessage)
        SendNotifications(Notif_2)
        return 1

    elif (valWL < 20 or valGas > 70 or ( (valLDR > 400) and (valLDR < 700) )):
        NotifMessage = " Washroom is becoming unusable, please check the Conditions.Water level is low, Gas is Unclean and There is sufficient luminosity.Suggestions:1). Check water Supply2). Check Whether the washroom is flushed"

        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC) 
        
        SendNotifications(NotifMessage);
        SendNotifications(Notif_2)
        return 2


    elif (valWL < 20 and valGas > 70 and ( (valLDR > 400) and (valLDR < 700) )):
        NotifMessage = " Washroom is becoming unusable, please check the Conditions.Water level is low, Gas is Unclean and There is sufficient luminosity.Suggestions:1). Check water Supply2). Check Whether the washroom is flushed"

        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC) 
        
        SendNotifications(NotifMessage);
        SendNotifications(Notif_2)
        return 2

    elif (((valWL < 60) and (valWL > 20)) and valGas > 70 and (valLDR > 700) ):
        NotifMessage = "Washroom is becoming unusable, please check the Conditions.\nWater level is Average, Gas is Unclean and There is not sufficient luminosity.Suggestions1). Check water Supply.2). Check Whether the washroom is flushed.3). Replace the broken bulbs if any."
        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC) 
        SendNotifications(NotifMessage);
        SendNotifications(Notif_2)
        return 3

    elif (valWL < 20 and valGas > 70 and (valLDR > 700) ):
        NotifMessage = "Washroom is becoming unusable, please check the Conditions.Water level is low, Gas is Unclean and There is not sufficient luminosity.Suggestions: 1). Check water Supply.2). Check Whether the washroom is flushed.3). Check whether bulb is proper or not."
        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC) 
        SendNotifications(Notif_2)
        SendNotifications(NotifMessage);
        return 4
    elif (valWL < 20 and valGas > 40 and ((valLDR < 300))):
        NotifMessage = "Washroom is becoming unusable, please check the Conditions.Water level is low, Gas is Moderately clean and There is More than enough luminosity.Suggestions: 1). Check water Supply. 2). Check Whether the washroom is flushed"
        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC)  
        SendNotifications(Notif_2)
        SendNotifications(NotifMessage);
        return 5
    elif (valWL > 20 and valWL < 60 and valGas > 70 and ( (valLDR > 300) and (valLDR < 700) )):
        NotifMessage = "Washroom is becoming unusable, please check the Conditions.Water level is Average, Gas is Unclean and There is Moderate luminosity.\n Suggestions: 2). Check Whether the washroom is flushed"
        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC)

        SendNotifications(Notif_2)
        SendNotifications(NotifMessage);
        return 6
    elif (valWL < 20 and valGas > 70 and ( (valLDR > 300) and (valLDR < 700) )):
        NotifMessage = "Washroom is becoming unusable, please check the Conditions.Water level is low, Gas is Unclean and There is sufficient luminosity.Suggestions: 1). Check water Supply. 2). Check Whether the washroom is flushed"
        
        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC) 
        SendNotifications(Notif_2)
        SendNotifications(NotifMessage);
        return 7

    elif(valPC > 150):
        Notif_2 = "Water Level = "+str(valWL)+"Gas Sensor: "+str(valGas)+"Illuminance: "+str(valLDR)+"Usage: "+str(valPC) 
        NotifMessage = """ Washroom has been used a lot, please look into it for once """
        SendNotifications(NotifMessage)
        SendNotifications(Notif_2)
        return 8
    
    else:
        print(" Nothing serious ^_^ ")
        return "k"

 
 


def SendNotifications(notifMessage):
    """Sends the Notifications""" 
    p.sendMessage(notifMessage,chat_id_group)

app.run(host='0.0.0.0',port = 50113)
