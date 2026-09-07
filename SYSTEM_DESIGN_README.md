### System Design Question: Payment Processing System

- Design a **payment processing system for an e-commerce platform**.
- Merchants submit payments using:
  - `POST /payments`
- The platform communicates with **external payment providers/banks** to charge customers.

## Requirements

- Support approximately **1,000 payment requests per second**.
- A customer must **never be charged twice**.
- Payment providers may:
  - Respond slowly.
  - Timeout.
  - Return ambiguous responses.
- Clients may **retry payment requests** if they don't receive a response.
- Payment states:
  - `PENDING`
  - `SUCCESS`
  - `FAILED`
- Merchants must be able to:
  - Query the status of a payment.
  - Receive a **webhook** when a payment completes.
- The system must maintain a complete **audit history** of every payment.
 