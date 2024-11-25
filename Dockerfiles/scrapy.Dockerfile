FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

# probably dont have to copy the whole directory
COPY . . 

WORKDIR /app/ufcstats

CMD ["sleep", "300"]