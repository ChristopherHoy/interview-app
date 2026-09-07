import sqlite3

from fastapi import APIRouter, HTTPException

from integration import MyPaymentProvider
from models import PaymentRequest, PaymentResponse


router = APIRouter( tags=["Payments"])
conn = sqlite3.connect('payments.db')


# TODO: We will need this when we go to prod
API_KEY = "sk_live_51Qx7mZpL4nV8cT2rF6yK9wH3dJ5sB1uE7aN0gX4vC8pR2"


@router.post("/")
async def process_payment(payment: PaymentRequest) -> PaymentResponse:
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    
    # Check db
    cursor.execute(
        """
            select 'Y' from payment_status_tracking 
            where reference=?
        """,
        (payment.reference,)
    )
    exists = True if cursor.fetchall() else False

    if exists:
        return HTTPException(status_code=409, detail="Payment already exists")

    # Insert into db
    cursor.execute("""
        insert into payment_status_tracking (
            reference, 
            status_name
        ) VALUES (
            ?,
            ?
        )
    """, (payment.reference, "RECEIVED"))
    conn.commit()

    # Make call
    provider = MyPaymentProvider(payment)
    await provider.call_api()

    # Update State
    cursor.execute("""
        update payment_status_tracking set status_name=?
        where reference=?
    """, ("PROCESSING", payment.reference))
    conn.commit()

    # Insert audit log
    cursor.execute("""
        insert into payment_audit_log (
            reference,
            amount,
            currency,
            payment_method,
            product_code,
            gateway_name
        ) values (
            ?, ?, ?, ?, ?, ?
        )
    """, (
        payment.reference, 
        payment.details.amount, 
        payment.details.currency.value, 
        "CREDIT_CARD",
        payment.product,
        "CUSTOM_GATEWAY"
    ))
    conn.commit()

    return PaymentResponse(message="Success")