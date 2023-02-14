from pydantic import BaseModel

class ussdRequest(BaseModel):
    session_id: int
    service_code: int
    phone_number: int
    text: str
    amount: int

class ussdResponse(BaseModel):
    session_id: int
    service_code: int
    phone_number: int

