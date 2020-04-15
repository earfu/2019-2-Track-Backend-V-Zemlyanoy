# 2019-2-Track-Backend-V-Zemlyanoy

Start:
- `git clone https://github.com/earfu/2019-2-Track-Backend-V-Zemlyanoy.git`
- `cd 2019-2-Track-Backend-V-Zemlyanoy`
- `docker-compose build`
- `docker-compose up`
- `make migrate`

Configuration files:
- ./messanger/application/settings.py
- ./messanger/application/local_settings.py
- ./messanger/application/flowerconfig.py
- ./centrifugo/centrifugo_config.json
- ./redis/redis.conf
- ./docker-compose.yml

Servers:
- Django http://127.0.0.1:8000
- Centrifugo http://127.0.0.1:8001
- Flower http://127.0.0.1:5555
- Postgres w/ Django ORM (use `make shell`)