# cmp_search

The search service. It is built using ELK stack

## Prerequisties

- Docker Desktop. Latest version of Docker is installed and running

## How to setup Elastic, Kibana

### Step 1 - Launch the docker compose

Run the below command on the terminal. If you are running it for the time, it will perform the necessary setup and run the service.

```shell
docker compose -f ./docker-compose-elastic.yml --env-file ./elastic.env -p cmp-elastic up -d
```

### Step 2 - Check Elastic, Kibana

Open the kibana dashboard
Launch the url https://localhost:5601 on the browser.
Use the below creds to logon. Refer to the elk.env file for details.
Username: elastic
Password: elasticpassword

If the setup is properly completed, you will be able to view the dashboard

### Step 3 - Create a new index

In Kibana, go to Elasticsearch
Choose New Index and create a test index named `first_test_index`

### Step 4 - Check the index in console

In Kibana, go to Dev Tools --> Console
Try the following command

```shell
get first_test_index/_search
```

You should see a response like this
{
"took": 1,
"timed_out": false,
"\_shards": {
"total": 1,
"successful": 1,
"skipped": 0,
"failed": 0
},
"hits": {
"total": {
"value": 0,
"relation": "eq"
},
"max_score": null,
"hits": []
}
}

### Step 5 - Injest test data

Try the below command in the console

```shell
PUT first_test_index/_doc/first_data_id_1?refresh
{
  "title": "Sample data",
  "subtitle": "My first sample",
  "view_count" : 1
}
```

### Step 6 - Sample search

Try the below command in the console

```shell
GET first_test_index/_search
{
  "query": {
    "match": {
      "title": "sample"
    }
  }
}
```

You should see a result.

### How to stop Elastic, Kibana

```shell
docker compose -f ./docker-compose-elastic.yml --env-file ./elastic.env -p cmp-elastic down
```

### How to setup Logstash

#### Step 1 - Build logstash

You need to build the custom logstash docker image. Ensure that you run this each time you make any changes to the Dockerfile.logstash

For building logstash

```shell
docker build -f ./Dockerfile.logstash -t cmp-logstash:latest .
```

#### Step 2 - Run logstash

For running logstash service. Make sure Elastic is up and running.

```shell
docker compose -f ./docker-compose-logstash.yml --env-file ./logstash.env -p cmp-logstash up -d
```

#### Step 3 - Stop logstash

```shell
docker compose -f ./docker-compose-logstash.yml --env-file ./logstash.env -p cmp-logstash down
```
