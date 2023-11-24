FROM python:3.11

COPY bitter /bitter/
COPY requirements.txt /bitter/requirements.txt
COPY configs/config.yml /configs/config.yml

WORKDIR /bitter

RUN pip install -r requirements.txt

ENV PYTHONPATH=/

CMD [ "python", "app.py" ]