FROM python:3.10

RUN apt-get update -y
RUN apt-get install -y wget unzip

# Install Chrome debian sources
RUN apt-get update \
    && apt-get install -y wget gnupg\
    && apt-get clean \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update \
    && apt-get install -y xvfb unzip openjdk-11-jre google-chrome-stable

# Install direct binary dependencies
#RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.2/browsermob-proxy-2.1.2-bin.zip \
RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip \
    && unzip browsermob-proxy-2.1.4-bin.zip \
    && wget http://selenium-release.storage.googleapis.com/2.41/selenium-server-standalone-2.41.0.jar \
    && wget https://chromedriver.storage.googleapis.com/111.0.5563.64/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && chmod +x chromedriver \
	&& cp chromedriver /usr/local/bin/

RUN pip install browsermob-proxy selenium xvfbwrapper

# Start selenium server
RUN mkdir -p /log \
    && /usr/bin/java -jar selenium-server-standalone-2.41.0.jar >> /log/selenium.$(date +"%Y%d%m").log 2>&1&

WORKDIR /src/

COPY app.py /src/

CMD ["python", "app.py"]

