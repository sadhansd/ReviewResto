FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY ./src/main.py .
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]