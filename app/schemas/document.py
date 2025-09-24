from pydantic import BaseModel
from typing import List


class Address(BaseModel):
    name: str
    street: str
    number: str = ""
    neighborhood: str = ""
    city: str
    state: str
    postal_code: str


class SenderRecipientPair(BaseModel):
    sender: Address
    recipient: Address


class DocumentRequest(BaseModel):
    pairs: List[SenderRecipientPair]


class DocumentResponse(BaseModel):
    message: str
    filename: str