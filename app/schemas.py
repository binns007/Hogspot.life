from pydantic import BaseModel, EmailStr
from datetime import datetime,time as Time, date
from typing import Dict, Optional, Union, Tuple

from fastapi import UploadFile
from fastapi import Form, File
from typing import List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    date_of_birth: date
    

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    date_of_birth: date
    is_verified: bool

    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email : EmailStr
    password : str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int



class HotspotCreate(BaseModel):
    name: str
    coordinates: List[Tuple[float, float]]
    status: bool 

class HotspotOut(BaseModel):
    id: int
    name: str
    coordinates: List[Tuple[float, float]]
    status: bool 

class Location(BaseModel):
    latitude: float
    longitude: float
