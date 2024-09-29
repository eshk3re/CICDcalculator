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
