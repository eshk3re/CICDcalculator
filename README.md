## Развертывание gitlab
Создаём docker-compose.yml для запуска контейнеров с gitlab и gitlab-runner:  
```yaml  
version: '2.6'
services:
  gitlab:
    image: gitlab/gitlab-ce:16.10.0-ce.0
    container_name: gitlab
    restart: always
    hostname: 'gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com'
    ports:
      - '80:80'
      - '443:443'
      - '22:22'
    volumes:
      - '/srv/gitlab/config:/etc/gitlab'
      - '/srv/gitlab/logs:/var/log/gitlab'
      - '/srv/gitlab/data:/var/opt/gitlab'
    shm_size: '256m'
    networks:
      - gitlab_net

  gitlab-runner:
    image: gitlab/gitlab-runner:alpine
    container_name: gitlab-runner
    restart: unless-stopped
    depends_on:
      - gitlab
    volumes:
      - /srv/gitlab-runner:/etc/gitlab-runner
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - gitlab_net

networks:
  gitlab_net:
    driver: bridge
```  
  
Запускаем контейнеры командой **docker compose up -d**

URL для перехода в gitlab через браузер: https://<ip-адрес машины>
![image](https://github.com/user-attachments/assets/d69e09a7-4965-42a8-aa84-f91b32e371b5)

Чтобы сбросить пароль рута и установить новый нужно выполнить следующие команды:
```
docker exec -it gitlab /bin/bash
cd /etc/gitlab
gitlab-rake "gitlab:password:reset[root]"
```
Заходим в `Admin area`, оттуда в `Users`, создадим пользователя с именем. Заходим в этого же пользователя, меняем пароль. После входа тоже потребуется смена.  
Создаем группу, в которой создаем репозиторий.
![image](https://github.com/user-attachments/assets/1bdfc200-4748-4de9-965f-763eee921e14)
  
Создаем ключи и серты в директории /srv/gitlab/config/ssl для корректной работы раннера
```
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 3654 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt
openssl req -newkey rsa:2048 -nodes -keyout gitlab.example.com.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=*.example.com" -out gitlab.example.com.csr
openssl x509 -req -extfile <(printf "subjectAltName=DNS:example.com,DNS:www.example.com,DNS:gitlab.example.com") -days 365 -in gitlab.example.com.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out gitlab.example.com.crt
```
Подкладываем в /srv/gitlab-runner ca.crt.
  
Регистрируем раннер:
```
docker exec -it gitlab-runner /bin/bash
gitlab-runner register --url "https://gitlab.example.com" --tls-ca-file=/etc/gitlab-runner/ca.crt --registration-token "<token>"
```
Token раннера необходимо создать в проекте -> Settings -> CI/CD -> Runners -> New project runner
![image](https://github.com/user-attachments/assets/ccf9291c-b64c-41c1-a0b5-74f96013a1b7)
  
Gitlab и gitlab-runner должны находится в одной сети.
  
**Далее пишем API-калькулятор на python с Flask, файл с зависимостями requirements.txt для работы калькулятора и Dockerfile для сборки калькулятора**
