FROM python:3.10

# Prereq. software
RUN apt update && apt upgrade -y && apt install build-essential -y

# Prereq.
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Code
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]