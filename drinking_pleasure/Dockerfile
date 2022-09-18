FROM python:3.8.5

ENV PYTHONUNBUFFERED 1

# 도커 컨테이너 내에서 코드가 실행될 경로 설정
RUN mkdir -p /home/ubuntu/Mazle/drinking_pleasure
WORKDIR /home/ubuntu/Mazle/drinking_pleasure

# 코드 실행될 경로에 requirments.txt 복사 후 설치
COPY ./requirements.txt /home/ubuntu/Mazle/drinking_pleasure/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r /home/ubuntu/Mazle/drinking_pleasure/requirements.txt

# 프로젝트를 code로 복사
COPY . .

CMD ["uwsgi", "--ini", "/home/ubuntu/Mazle/drinking_pleasure/config/uwsgi/uwsgi.ini"]

EXPOSE 8000
