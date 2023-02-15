from fastapi import FastAPI, HTTPException, status, File, UploadFile, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from typing import List,Optional
from fastapi.responses import HTMLResponse
from datetime import date, datetime
from cachetools import Cache
from models import*
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

# maxsize is the size of data the Cache can hold
cache_data = Cache(maxsize=50000)


# Connect to the MongoDB database
#client = MongoClient('mongodb+srv://code_god:rootadmin@aoristai.1ofe1s4.mongodb.net/test')
#db = client['airworks']

app = FastAPI()

response = ""

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/ussd")
async def handle_ussd(ussdRequest: UssdRequest):
    response = UssdResponse(
        sessionID=ussdRequest.sessionID,
        userID=ussdRequest.userID,
        msisdn=ussdRequest.msisdn,
    )

    if ussdRequest.newSession:
        response.message = (
            "Select an option"
            + "\n1. Buy Airtime"
            + "\n2. Buy SMS"
            + "\n3. Buy Data"
            + "\n4. Buy Minutes"
        )

        response.continueSession = True

        # Keep track of the USSD state of the user and their session

        current_state = UssdState(
            sessionID=ussdRequest.sessionID,
            msisdn=ussdRequest.msisdn,
            userData=ussdRequest.userData,
            network=ussdRequest.network,
            message=response.message,
            level=1,
            part=1,
            newSession=True,
        )

        user_response_tracker = cache_data.get(hash(ussdRequest.sessionID), [])

        user_response_tracker.append(current_state)

        cache_data[hash(ussdRequest.sessionID)] = user_response_tracker
    else:
        last_response = cache_data.get(hash(ussdRequest.sessionID), [])[-1]

        if last_response.level == 1:
            user_data = ussdRequest.userData

            if user_data == "1":
                response.message = (
                    "Enter Phone Number"
                )
                response.continueSession = True

                # Keep track of the USSD state of the user and their session

                current_state = UssdState(
                    sessionID=ussdRequest.sessionID,
                    msisdn=ussdRequest.msisdn,
                    userData=ussdRequest.userData,
                    network=ussdRequest.network,
                    message=response.message,
                    level=2,
                    part=1,
                    newSession=ussdRequest.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussdRequest.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussdRequest.sessionID)] = user_response_tracker
            elif (
                user_data == ussd.phone_number
            ):
                response.message = "Thank you for voting!"
                response.continueSession = False
            else:
                response.message = "Bad choice!"
                response.continueSession = False
        elif last_response.level == 2:
            possible_choices = ["1", "2", "3", "4"]

            if last_response.part == 1 and ussdRequest.userData == "#":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n3. Bulk SMS"
                    + "\n\n*. Go Back"
                    + "\n#. Next Page"
                )
                response.continueSession = True

                current_state = UssdState(
                    sessionID= ussdRequest.sessionID,
                    msisdn=ussdRequest.msisdn,
                    userData=ussdRequest.userData,
                    network=ussdRequest.network,
                    message=response.message,
                    level=2,
                    part=2,
                    newSession=ussdRequest.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussdRequest.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussdRequest.sessionID)] = user_response_tracker
            elif last_response.part == 2 and ussdRequest.userData == "#":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n4. SMS To Contacts"
                    + "\n\n*. Go Back"
                )
                response.continueSession = True

                current_state = UssdState(
                    sessionID=ussdRequest.sessionID,
                    msisdn=ussdRequest.msisdn,
                    userData=ussdRequest.userData,
                    network=ussdRequest.network,
                    message=response.message,
                    level=2,
                    part=3,
                    newSession=ussdRequest.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussdRequest.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussdRequest.sessionID)] = user_response_tracker
            elif last_response.part == 3 and ussdRequest.userData == "*":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n3. Bulk SMS"
                    + "\n\n*. Go Back"
                    + "\n#. Next Page"
                )
                response.continueSession = True

                current_state = UssdState(
                    sessionID=ussdRequest.sessionID,
                    msisdn=ussdRequest.msisdn,
                    userData=ussdRequest.userData,
                    network=ussdRequest.network,
                    message=response.message,
                    level=2,
                    part=2,
                    newSession=ussdRequest.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussdRequest.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussdRequest.sessionID)] = user_response_tracker
            elif last_response.part == 2 and ussdRequest.userData == "*":
                response.message = (
                    "For SMS which of the features do you like best?"
                    + "\n1. From File"
                    + "\n2. Quick SMS"
                    + "\n\n #. Next Page"
                )
                response.continueSession = True

                # Keep track of the USSD state of the user and their session

                current_state = ussdState(
                    sessionID=ussdRequest.sessionID,
                    msisdn=ussdRequest.msisdn,
                    userData=ussdRequest.userData,
                    network=ussdRequest.network,
                    message=response.message,
                    level=2,
                    part=1,
                    newSession=ussdRequest.newSession,
                )

                user_response_tracker = cache_data.get(hash(ussdRequest.sessionID), [])

                user_response_tracker.append(current_state)

                cache_data[hash(ussdRequest.sessionID)] = user_response_tracker
            elif ussdRequest.userData in possible_choices:
                response.message = "Thank you for voting!"
                response.continueSession = False
            else:
                response.message = "Bad choice!"
                response.continueSession = False

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
