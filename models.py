from pydantic import BaseModel

class ussd(BaseModel):
    session_id: int
    service_code: int
    phone_number: int
    text: str
    amount: int

class UssdRequest(BaseModel):
    sessionID: str
    userID: str
    newSession: bool
    msisdn: str
    userData: str | None = None
    network: str


class UssdResponse(BaseModel):
    sessionID: str | None = None
    userID: str | None = None
    continueSession: bool | None = None
    msisdn: str | None = None
    message: str | None = None


class UssdState(BaseModel):
    sessionID: str
    message: str
    newSession: bool
    msisdn: str
    userData: str | None = None
    network: str
    message: str
    level: int
    part: int

