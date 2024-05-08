FROM python:bullseye

WORKDIR /app

RUN pip install --upgrade pip

COPY . /app/

EXPOSE 4221

CMD python app/main.py