FROM paas-images.epam.com/proxy/library/python:3.8

ARG BRANCH_NAME=""

WORKDIR /clocker-tests

COPY requirements.txt /
COPY . .
COPY docker_entrypoint.sh /

ENV PYTHONPATH="."
ENV CI_SERVER="yes"

RUN apt-get update
RUN apt-get -y install gdebi-core
RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_88.0.4324.96-1_amd64.deb
RUN gdebi -n ./google-chrome*.deb || echo "Error on installing google chrome"
RUN pip3 install -r requirements.txt

RUN chmod +x docker_entrypoint.sh

CMD ['export', 'export', 'PYTHONPATH="$(pwd)"']
ENTRYPOINT ["./docker_entrypoint.sh"]
