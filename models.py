from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Currency(Enum):
    ZAR = "ZAR"


class BillingAddress(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str
    line2: Optional[str] = None 


class PaymentDetails(BaseModel):
    currency: Currency
    amount: float
    card_number: str
    cvv: str
    cardholder: str
    expiry: datetime
    billing_address: BillingAddress
    

class PaymentRequest(BaseModel):
    reference: str
    product: str
    details: PaymentDetails


class PaymentResponse(BaseModel):
    message: str