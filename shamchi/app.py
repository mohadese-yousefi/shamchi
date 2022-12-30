import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from bson import ObjectId
import motor.motor_asyncio


app = FastAPI()
DATABASE_URL = os.environ.get('DATABASE_URL')
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client.shamchi


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Food(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Kabab",
                "enable": True,
            }
        }

@app.get(
     "/", response_description="Get one random food", response_model=Food)
async def get_food():
    '''Get the random food'''
    return JSONResponse(status_code=status.HTTP_200_OK, content=Food)


