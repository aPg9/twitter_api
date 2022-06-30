from uuid import UUID 
#Pydantic
from pydantic import BaseModel 
from pydantic import EmailStr
from pydantic import Field
# Fastapi
from fastapi import FastAPI

app = FastAPI()

# Models

class User(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class Tweet(BaseModel):
    pass

@app.get(path="/")
def home():
    return {"twitter API": "Working!"}