FROM python:3

RUN mkdir -p /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt &&\
  apt-get update &&\
  apt-get -y install dvipng texlive-latex-extra texlive-latex-recommended texlive-base

CMD python3 main.py $(cat /run/secrets/omegabot-token)
