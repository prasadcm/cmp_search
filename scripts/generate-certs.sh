#!/bin/bash

set -e

CERT_DIR=./certs

echo "Creating CA..."
mkdir -p $CERT_DIR/ca
openssl genrsa -out $CERT_DIR/ca/ca.key 4096
openssl req -x509 -new -nodes -key $CERT_DIR/ca/ca.key -sha256 -days 3650 \
  -subj "/CN=Elastic Dev CA" \
  -out $CERT_DIR/ca/ca.crt

echo "Creating Elasticsearch certificate..."
mkdir -p $CERT_DIR/es01
openssl genrsa -out $CERT_DIR/es01/es01.key 4096
openssl req -new -key $CERT_DIR/es01/es01.key -subj "/CN=es01" -out $CERT_DIR/es01/es01.csr
openssl x509 -req -in $CERT_DIR/es01/es01.csr -CA $CERT_DIR/ca/ca.crt -CAkey $CERT_DIR/ca/ca.key \
  -CAcreateserial -out $CERT_DIR/es01/es01.crt -days 365 -sha256 \
  -extfile <(echo "subjectAltName = DNS:es01,DNS:localhost,DNS:host.docker.internal,IP:127.0.0.1")

echo "Creating Kibana certificate..."
mkdir -p $CERT_DIR/kibana
openssl genrsa -out $CERT_DIR/kibana/kibana.key 4096
openssl req -new -key $CERT_DIR/kibana/kibana.key -subj "/CN=kibana" -out $CERT_DIR/kibana/kibana.csr
openssl x509 -req -in $CERT_DIR/kibana/kibana.csr -CA $CERT_DIR/ca/ca.crt -CAkey $CERT_DIR/ca/ca.key \
  -CAcreateserial -out $CERT_DIR/kibana/kibana.crt -days 365 -sha256 \
  -extfile <(echo "subjectAltName = DNS:kibana,IP:127.0.0.1")

echo "Creating Logstash certificate..."
mkdir -p $CERT_DIR/logstash
openssl genrsa -out $CERT_DIR/logstash/logstash.key 4096
openssl req -new -key $CERT_DIR/logstash/logstash.key -subj "/CN=logstash" -out $CERT_DIR/logstash/logstash.csr
openssl x509 -req -in $CERT_DIR/logstash/logstash.csr -CA $CERT_DIR/ca/ca.crt -CAkey $CERT_DIR/ca/ca.key \
  -CAcreateserial -out $CERT_DIR/logstash/logstash.crt -days 365 -sha256 \
  -extfile <(echo "subjectAltName = DNS:logstash,IP:127.0.0.1")

echo "Done! Certificates are in $CERT_DIR"
