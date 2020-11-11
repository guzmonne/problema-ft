# Load .env from
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: up down restart build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

restart: down up

build:
	cd api && docker build -t guzmonne/problema-ft:${VERSION} .

metricbeat:
	docker run \
		--network ${DOCKER_NETWORK} \
		docker.elastic.co/beats/metricbeat:7.9.3 \
		setup -E setup.kibana.host=kibana:5601 \
		-E output.elasticsearch.hosts=["elasticsearch:9200"]
