
# Simple curl to test endpoint
curl -XPOST localhost:8000/ --json @samples/payment.json


# Simple curl to test supplier
curl -XPOST localhost:8092/process --data {}