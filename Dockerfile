FROM python:3.8

ARG BRANCH_NAME=""

WORKDIR /clocker-tests

COPY requirements.txt /
COPY . .

ENV PYTHONPATH="."
ENV CI_SERVER="yes"

RUN apt-get update
RUN apt-get -y install gdebi-core
RUN pip3 install -r requirements.txt

ENV GLOBAL_VARIABLE="your_value"

# Добавляем CMD команду для вывода значения переменной TEST_KEY
CMD echo "TEST_KEY=$TEST_KEY"
