FROM python:3.8-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update -y -q


# adding chrome to source list
# https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#running-puppeteer-in-docker
RUN  apt-get install -y wget gnupg \
	&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | \
	gpg -q --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/78BD65473CB3BD13.gpg --import \
	&& chmod 644 /etc/apt/trusted.gpg.d/78BD65473CB3BD13.gpg \
	&& sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

# installing chrome binary and additional fonts 
RUN apt-get update \
	&& apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN pip3 install psycopg2-binary
RUN pyppeteer-install

COPY ./ /app

RUN mkdir -p /app/logs
RUN mkdir -p /app/media

CMD ["python", "bot.py"]
