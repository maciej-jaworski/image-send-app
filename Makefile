COMPOSE=docker compose -f docker-compose.yml

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up

bash:
	$(COMPOSE) run backend bash

test:
	$(COMPOSE) run backend test
