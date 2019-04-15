import flask 
from flask import request,jsonify,render_template
import Module.poop as poop
import pickle

# buffer variables
# are meant to be declared here, we will share the stuffs 
# with botogram bot!

primary_Gasbuffer = []
primary_LDRbuffer = []
usageCounter = []
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
                
                print(valGas+" "+valLDR+" "+valPC)
                primary_Gasbuffer.append(valGas)
                primary_LDRbuffer.append(valLDR)
                usageCounter.append(valPC)
    
                gasBuffer = "file_gas"
                gas_object = open(gasBuffer, 'wb')
                ldrBuffer = "file_ldr"
                ldr_object = open(ldrBuffer, 'wb')
                pcBuffer = "file_pc"
                pc_object = open(pcBuffer, 'wb')
                #Stuffs ^ 
                pickle.dump(primary_Gasbuffer,gas_object)
                pickle.dump(primary_LDRbuffer,ldr_object)
                pickle.dump(usageCounter,pc_object)
                gas_object.close()
                ldr_object.close()
                pc_object.close()
                return ""
    else:
        return " "

    

    

app.run(host='0.0.0.0')
