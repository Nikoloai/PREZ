FROM node:20-bullseye-slim

RUN npm install -g @marp-team/marp-cli

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
