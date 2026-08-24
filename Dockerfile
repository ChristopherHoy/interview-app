FROM python:3.12-slim


WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Specify the command to run your app (replace app.py with your entry point)
CMD ["python", "main.py"]