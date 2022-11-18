# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 14:48:56 2021

@author: Diana
"""

from flask import Flask
import os
from twilio.rest import Client
from flask import request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app =Flask(__name__)

@app.route("/hola")
def inicio():
    test =os.environ.get("Test")
    return test()

@app.route ("/sms")
def sms():
    try:
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        
        contenido = request.args.get("mensaje")
        destino = request.args.get("telefono")
        message = client.messages \
                        .create(
                             body=contenido,
                             from_='+18783029971',
                             to='+57'+ destino
                         )
        
        print(message.sid)
        return "Enviado correctamente"
    except Exception as e:
        return "El mensaje no se pudo enviar"

@app.route("/envio-correo")
def email():
    
    destino=request.args.get("correo_destino")
    asunto=request.args.get("asunto")
    mensaje=request.args.get("contenido")
    
    message = Mail(
    from_email='progwebmintic@gmail.com',
    to_emails= destino,
    subject=asunto,
    html_content=mensaje)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return "E-mail enviado"
    except Exception as e:
        print(e.message)
        return "Error enviando E-mail"
    

if __name__ == "__main__":
    port = int(os.environment.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
