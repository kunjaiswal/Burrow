export PATH=$PATH:/usr/local/bin

export BROKERS=$(echo $VCAP_SERVICES | jq -r .kafka[0].credentials.cluster.brokers)
export ZK=$(echo $VCAP_SERVICES | jq -r .kafka[0].credentials.cluster.zk)
export  USERNAME=$(echo $VCAP_SERVICES | jq -r .kafka[0].credentials.username)

export PASSWORD=$(echo $VCAP_SERVICES | jq -r .kafka[0].credentials.password)
export  CA_CERT_URL=$(echo $VCAP_SERVICES | jq -r .kafka[0].credentials.urls.ca_cert)

export TOKEN_URL=$(echo $VCAP_SERVICES | jq -r .kafka[0].credentials.urls.token)

curl -s -o rootCA.crt $(echo $VCAP_SERVICES | jq -r .kafka[0].credentials.urls.ca_cert) 

export TOKEN=$(curl  -sS -X POST \
  $TOKEN_URL \
  -u $USERNAME:$PASSWORD \
  -H 'cache-control: no-cache' \
  -H 'charset: utf-8' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -d grant_type=client_credentials | jq -r .access_token) 

echo "your setup script ran correctly ---"
