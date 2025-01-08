FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY ./src .
RUN pip install -r requirements.txt
CMD [ "streamlit","run", "app.py" ]