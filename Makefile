# Load .env from
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

create-directories:
	mkdir -p ${PROJECT_PATH} \
		${PROJECT_PATH}/certificates \
		${PROJECT_PATH}/elasticsearch \
		${PROJECT_PATH}/redis \
		${PROJECT_PATH}/apm \
		${PROJECT_PATH}/metricbeat \
		${PROJECT_PATH}/redis

ln-metricbeat:
	ln ./configurations/metricbeat.docker.yml ${PROJECT_PATH}/metricbeat/metricbeat.docker.yml

ln-apm:
	ln ./configurations/apm-server.docker.yml ${PROJECT_PATH}/apm/apm-server.docker.yml

change-owner:
	chown -R 1000:1000 ${PROJECT_PATH}				;\
	chown -R 0:0 ${PROJECT_PATH}/apm					;\
	chown -R 0:0 ${PROJECT_PATH}/metricbeat   ;\
	chown -R 0:0 ${PROJECT_PATH}/redis

setup: create-directories ln-metricbeat ln-apm change-owner

clean:
	rm -Rf ${PROJECT_PATH}

.PHONY: setup create-directories ln-metricbeat ln-apm change-owner clean

recreate:
	/usr/local/bin/docker-compose up -d --force-recreate

up:
	/usr/local/bin/docker-compose up -d

down:
	/usr/local/bin/docker-compose down --remove-orphans

restart: down up

metricbeat:
	docker run \
		--network ${DOCKER_NETWORK} \
		docker.elastic.co/beats/metricbeat:7.9.3 \
		setup -E setup.kibana.host=kibana:5601 \
		-E output.elasticsearch.hosts=["elasticsearch:9200"]

.PHONY: up down restart recreate metricbeat
