FROM python:3.8

RUN mkdir -p /bot/
WORKDIR /bot/

COPY ./requirements.txt /bot/

RUN pip3 install -r requirements.txt

COPY . /bot/

CMD ["python3", "-m", "bot_top_ranking"]
