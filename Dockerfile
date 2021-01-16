FROM python:alpine

RUN pip install uvicorn fastapi arrow requests bs4

COPY dandan.py /dandan.py

EXPOSE 8080

CMD [ "python", "dandan.py", "host=0.0.0.0", "port=8080" ]