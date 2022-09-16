FROM nginx:latest

# 기존 도커의 nginx 설정 파일 변경
COPY nginx.conf /etc/nginx/

COPY nginx-app.conf /etc/nginx/conf.d/ 

CMD ["nginx", "-g", "daemon off;"]
