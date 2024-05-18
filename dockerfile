FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt &&\
  apt-get update &&\
  apt-get install -y --no-install-recommends dvipng texlive-latex-base texlive-latex-extra &&\
  apt-get autoremove -y

CMD python3 main.py $(cat /run/secrets/omegabot-token)
