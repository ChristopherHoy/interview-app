from dataclasses import dataclass
import httpx
from models import PaymentRequest

@dataclass
class PaymentProvider:
    name: str
    base_url: str
    path: str

    payment: PaymentRequest

    @property
    def payload(self) -> str:
        return self.payment.details.model_dump_json()

    async def call_api(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/{self.path}", json=self.payload)
            response.raise_for_status()
            return response.json()


@dataclass
class MyPaymentProvider():
    name: str = "MY_PAYMENT_PROVIDER"
    base_url: str = "http://localhost:8092"
    path: str = "/process"