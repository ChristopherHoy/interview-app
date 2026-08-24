import sqlite3

from fastapi import APIRouter, HTTPException

from integration import PaymentProvider
from models import PaymentRequest, PaymentResponse


router = APIRouter(prefix="/process", tags=["Payments"])
conn = sqlite3.connect('payments.db')


@router.post("/")
async def process_payment(payment: PaymentRequest) -> PaymentResponse:
    conn = sqlite3.connect("payments.db")
    cursor = conn.cursor()
    
    # Check db
    cursor.execute(
        """
            select 'Y' as exists from payment_status_tracking 
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
    provider = PaymentProvider(payment)
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
            gateway_name,
        ) values (
            ?, ?, ?, ?, ?, ?
        )
    """, (
        payment.reference, 
        payment.details.amount, 
        payment.details.currency, 
        "CREDIT_CARD",
        payment.product,
        "CUSTOM_GATEWAY"
    ))
    conn.commit()

    return PaymentResponse(message="Success")