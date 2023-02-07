from fastapi import FastAPI, HTTPException, status, File, UploadFile, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List,Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import uvicorn
import requests
import africastalking

#initiating the airtime api
username = "Praise Godwins"   #YOUR_USERNAME_GOES_HERE"
api_key = "0400606da5dc0bb3c11596d85d645b5f419c2e845b766750b22d8b8f0d6a5a34"  #YOUR_APIKEY_GOES_HERE

africastalking.initialize(username, api_key)
airtime = africastalking.Airtime

phone_number = "YOUR_PHONE_NUMBER_GOES_HERE"
amount = 300
currency_code = "KES"


# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017')
db = client['airworks']

app = FastAPI()

response = ""

class ussd(BaseModel):
    session_id: int
    service_code: int
    phone_number: int
    text: str
    amount: int

@app.get("/")
async def read_root():
    return {"Hello": "World"}
    


@app.get("/ussd/")
def ussd_callback(ussd: ussd, request: Request, api_key: str = Header(None)):
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    amount = ussd.amount
    currency_code = "KES"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apiKey": api_key
    }

    if text == '':
        response  = "CON Send instructions \n"
        response += "1. Buy airtime \n"
        response += "2. Buy sms \n"
        response += "3. Buy data \n"
        response += "4. BUy minutes"

    elif text == '1':
        response = "CON send instructions \n"
        response += "1. Enter phone number"
        

    elif text == '1*1':
        response = "CON enter phone number \n"
        phone_number += ""
        try:
            response = airtime.send(phone_number=phone_number, amount=amount, currency_code=currency_code)
            print(response)
        except Exception as e:
            print(f"Encountered an error while sending airtime. More error details below\n {e}")

    else:
        response = "CON service not available"

    data = {
        "username": "MyAppUserName",
        "productName": "myProductName",
        "recipients": [{
            "phoneNumber": phone_number,
            "currencyCode": "KES",
            "amount": amount,
            "metadata": {
                "foo": "bar",
                "key": "value"
            },
            "reason": "paymentsReason"
        }]
    }

    response = requests.post(
        "https://payments.sandbox.africastalking.com/mobile/b2c/request",
        headers=headers,
        json=data
    )

    return response

@app.post("/ussd/")
async def ussd_callback(ussd: ussd, request: Request, api_key: str = Header(None)):
    global response
    session_id = ussd.session_id
    service_code = ussd.service_code
    phone_number = ussd.phone_number
    amount = ussd.amount
    text = ussd.text

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apiKey": api_key
    }

    if text == '':
        response  = "CON Send instructions \n"
        response += "1. Buy airtime \n"
        response += "2. Buy sms \n"
        response += "3. Buy data \n"
        response += "4. BUy minutes"

    elif text == '1':
        response = "CON send instructions \n"
        response += "1. Enter phone number"
        

    elif text == '1*1':
        response = "CON enter phone number \n"
        phone_number += ""
        try:
            response = airtime.send(phone_number=phone_number, amount=amount, currency_code=currency_code)
            print(response)
        except Exception as e:
            print(f"Encountered an error while sending airtime. More error details below\n {e}")

    else:
        response = "CON service not available"

    data = {
        "username": "MyAppUserName",
        "productName": "myProductName",
        "recipients": [{
            "phoneNumber": phone_number,
            "currencyCode": "KES",
            "amount": amount,
            "metadata": {
                "foo": "bar",
                "key": "value"
            },
            "reason": "paymentsReason"
        }]
    }

    response = requests.post(
        "https://payments.sandbox.africastalking.com/mobile/b2c/request",
        headers=headers,
        json=data
    )

    return response

@app.post("/mobile/b2c/request")
async def send_mobile_b2c_payment_request(request: Request, api_key: str = Header(None)):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apiKey": api_key
    }
    data = {
        "username": "MyAppUserName",
        "productName": "myProductName",
        "recipients": [{
            "phoneNumber": phone_number,
            "currencyCode": "KES",
            "amount": amount,
            "metadata": {
                "foo": "bar",
                "key": "value"
            },
            "reason": "paymentsReason"
        }]
    }
    response = requests.post(
        "https://payments.sandbox.africastalking.com/mobile/b2c/request",
        headers=headers,
        json=data
    )
    return response.json()


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
