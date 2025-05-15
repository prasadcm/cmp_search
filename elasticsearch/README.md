# Elasticsearch

The docker version of elasticsearch is used to setup the search platform

## Prerequisties

- Docker engine. Latest version of Docker is installed and running. For local development install docker desktop.
- The below steps are tested on MacOS. Need to validate for windows

## Setup certificates for local development. For production deployments, use trusted certificates from CA

Run the shared/scripts/generate-certs.sh to generate the certs for elastic, kibana, logstash

```shell
cd shared
./scripts/generate-certs.sh
cd ..
```

## Setup Elastic, Kibana

### Step 1 - Launch the docker compose

Run the below command on the terminal. If you are running it for the time, it will perform the necessary setup and run the service.

```shell
cd elastic
docker compose -f ./docker-compose-elastic.yml --env-file ./elastic.env -p cmp-elastic up -d
cd ..
```

If all goes well, you should following output

```shell
[+] Running 4/4
 ⠿ Network cmp-elastic_cmp-elastic               Created
 ⠿ Container cmp-elastic-es01-1                  Healthy
 ⠿ Container cmp-elastic-kibana-password-init-1  Exited
 ⠿ Container cmp-elastic-kibana-1                Started
```

### Step 2 - Check Elastic, Kibana

Open the kibana dashboard
Launch the url https://localhost:5601 on the browser. If you get Untrusted error, go to keychain access and Trust the "Elastic Dev CA" certificate.
Use the below creds to logon. Refer to the elk.env file for details.
Username: elastic
Password: [password]

If the setup is properly completed, you will be able to view the dashboard

### Step 3 - Perform some basic checks

In Kibana, Go to Dev Tools --> Console
Try the following command

#### Create a new index

```shell
PUT /first_test_index
```

You should see a output like this

```shell
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "index": "first_test_index"
}
```

#### Injest test data

```shell
PUT first_test_index/_doc/first_data_id_1?refresh
{
  "title": "Sample data",
  "subtitle": "My first sample",
  "view_count" : 1
}
```

#### Perform search

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

You should see a result like this

```shell
  {
    "took": 7,
    "timed_out": false,
    "_shards": {
      "total": 1,
      "successful": 1,
      "skipped": 0,
      "failed": 0
    },
    "hits": {
      "total": {
        "value": 1,
        "relation": "eq"
      },
      "max_score": 0.2876821,
      "hits": [
        {
          "_index": "first_test_index",
          "_id": "first_data_id_1",
          "_score": 0.2876821,
          "_source": {
            "title": "Sample data",
            "subtitle": "My first sample",
            "view_count": 1
          }
        }
      ]
    }
  }
```

### Stopping Elastic, Kibana

Run the below command in terminal

```shell
docker compose -f ./docker-compose-elastic.yml --env-file ./elastic.env -p cmp-elastic down
```
