FROM --platform=linux/amd64 ubuntu:22.04

WORKDIR /

COPY ./requirements.txt ./requirements.txt

RUN apt-get update

RUN apt-get -y install wget unzip cmake libc6-dev-i386 g++-multilib patch imagemagick exiftool python3-pip

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]