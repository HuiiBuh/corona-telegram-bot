FROM python:3.8

WORKDIR /bot
COPY ["src", "requirements.txt", "/bot/"]
RUN pip install --no-cache-dir -r requirements.txt

ENV DB_LOCATION "/database"
ENV PRODUCTION True

CMD python /bot/main.py
