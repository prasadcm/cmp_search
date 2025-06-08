# Logstash

The search platform uses logstash to injest data into elasticsearch database.

## Prerequisties

- Docker engine. Latest version of Docker is installed and running. For local development install docker desktop.
- The below steps are tested on MacOS. Need to validate for windows.
- Elasticsearch is up and running. Refer to README of elasticsearch folder.
- The certificates are generated. This will be done when you follow the elasticsearch setup.

## Setup

### Build logstash

You need to build the custom logstash docker image. Ensure that you run this each time you make any changes to the pipelines, templates

Run the below command in terminal

```shell
cd logstash
docker build -f ./Dockerfile.logstash -t cmp-logstash:latest .
```

### Run logstash

Run the below command in terminal

```shell
docker compose -f ./docker-compose-logstash.yml --env-file ./logstash.env -p cmp-logstash up -d
```

## Stop logstash

Run the below command in terminal

```shell
docker compose -f ./docker-compose-logstash.yml --env-file ./logstash.env -p cmp-logstash down
```
