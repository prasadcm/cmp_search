#!/bin/bash

set -e

CERT_DIR=./certs
DAYS_VALID=365

echo "Creating CA..."
mkdir -p $CERT_DIR/ca

# Generate CA key and self-signed certificate
openssl genrsa -out $CERT_DIR/ca/ca.key 4096
openssl req -x509 -new -nodes -key $CERT_DIR/ca/ca.key \
  -subj "/CN=Elastic Dev CA" \
  -days 3650 -sha256 -out $CERT_DIR/ca/ca.crt

generate_cert () {
  NAME=$1
  COMMON_NAME=$2
  ALT_NAMES=$3

  echo "Creating certificate for $NAME..."
  mkdir -p $CERT_DIR/$NAME

  # Key
  openssl genrsa -out $CERT_DIR/$NAME/$NAME.key 4096

  # CSR
  openssl req -new -key $CERT_DIR/$NAME/$NAME.key -subj "/CN=$COMMON_NAME" \
    -out $CERT_DIR/$NAME/$NAME.csr

  # Extension file
  cat > $CERT_DIR/$NAME/extfile.cnf <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = $ALT_NAMES
EOF

  # Signed cert
  openssl x509 -req -in $CERT_DIR/$NAME/$NAME.csr \
    -CA $CERT_DIR/ca/ca.crt -CAkey $CERT_DIR/ca/ca.key -CAcreateserial \
    -out $CERT_DIR/$NAME/$NAME.crt -days $DAYS_VALID -sha256 \
    -extfile $CERT_DIR/$NAME/extfile.cnf
}

# Generate for each service
generate_cert "es01" "es01" "DNS:es01,DNS:localhost,DNS:host.docker.internal,IP:127.0.0.1"
generate_cert "kibana" "kibana" "DNS:kibana,DNS:localhost,IP:127.0.0.1"
generate_cert "logstash" "logstash" "DNS:logstash,IP:127.0.0.1"

echo "✅ Done! Certificates are in $CERT_DIR"
