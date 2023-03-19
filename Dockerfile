FROM python:3.10


RUN apt-get update -y
RUN apt-get install -y wget unzip

# Install Chrome debian sources
RUN apt-get update \
    && apt-get install -y wget gnupg\
    && apt-get clean \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# Install Chrome and openjdk
RUN apt-get update \
    && apt-get install -y xvfb unzip openjdk-11-jre google-chrome-stable

# Install direct binary dependencies
# BrowserMobProxy
# Selenium
# Chrome Driver
RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip \
    && unzip browsermob-proxy-2.1.4-bin.zip \
    && wget http://selenium-release.storage.googleapis.com/2.41/selenium-server-standalone-2.41.0.jar \
    && wget https://chromedriver.storage.googleapis.com/111.0.5563.64/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && chmod +x chromedriver \
	&& cp chromedriver /usr/local/bin/

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src/

COPY requirements.txt /src/requirements.txt

RUN pip install -r requirements.txt
