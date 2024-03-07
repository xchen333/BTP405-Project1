FROM python:latest

WORKDIR /app

RUN mkdir -p /app/database/
RUN mkdir -p /app/server/
RUN mkdir -p /app/utils/

COPY main.py /app/
COPY nginx.conf /app/
COPY database/ /app/database/
COPY server/ /app/server/
COPY utils/ /app/utils/

RUN pip install --upgrade pip
RUN pip install "psycopg[binary,pool]"
RUN pip install sqlalchemy

EXPOSE 80 443

CMD python main.py
