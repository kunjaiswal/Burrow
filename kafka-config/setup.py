import os,json,toml

test = '{"kafka":[{"label":"kafka","provider":null,"plan":"dedicated","name":"test_kafka","tags":["kafka"],"instance_name":"test_kafka","binding_name":null,"credentials":{"username":"sbss_9rjwy-anhzeepowwv3elib5bnexa53ixfkn9hwgtu25szzj2u32xdycg1chevfbmu2q=","password":"aa_gzwnmonQR7xNJLBt6fg321Bv4MI=","urls":{"ca_cert":"https://kafka-service-broker.cf.sap.hana.ondemand.com/certs/rootCA.crt","token":"https://kafka-service-oauth.cf.sap.hana.ondemand.com/v1/39976793-dd2d-411a-bdf8-5504188dd84b/token","token_key":"https://kafka-service-oauth.cf.sap.hana.ondemand.com/v1/token_key","service":"https://kafka-service.cf.sap.hana.ondemand.com/v1/39976793-dd2d-411a-bdf8-5504188dd84b"},"cluster":{"zk":"10.254.20.10:2181,10.254.20.11:2181,10.254.20.12:2181","brokers":"10.254.20.21:9093,10.254.20.22:9093,10.254.20.23:9093","brokers.auth_ssl":"10.254.20.21:9093,10.254.20.22:9093,10.254.20.23:9093"},"tenant":"39976793-dd2d-411a-bdf8-5504188dd84b"},"syslog_drain_url":null,"volume_mounts":[]}]}'
NOTIFIER_FROM= os.getenv("NOTIFIER_FROM")
NOTIFIER_GROUP_WHITELIST = os.getenv("NOTIFIER_GROUP_WHITELIST")
NOTIFIER_INTERVAL= os.getenv("NOTIFIER_INTERVAL")
NOTIFIER_PASSWORD= os.getenv("NOTIFIER_PASSWORD")
NOTIFIER_SERVER= os.getenv("NOTIFIER_SERVER")
NOTIFIER_THRESHOLD= os.getenv("NOTIFIER_THRESHOLD")
NOTIFIER_TO= os.getenv("NOTIFIER_TO")
NOTIFIER_USERNAME= os.getenv("NOTIFIER_USERNAME")


vcap_services = os.environ['VCAP_SERVICES']
datastore = json.loads(vcap_services)
zk1 = datastore['kafka'][0]['credentials']['cluster']['zk']
#open file to read
f = open("burrow.toml", "r")
s = f.read()
data_item = toml.loads(s)
data_item['notifier']['default']['interval'] =NOTIFIER_INTERVAL
data_item['notifier']['default']['threshold'] =NOTIFIER_THRESHOLD
data_item['notifier']['default']['server'] =NOTIFIER_SERVER
data_item['notifier']['default']['from'] =NOTIFIER_FROM
data_item['notifier']['default']['to'] =NOTIFIER_TO
data_item['notifier']['default']['username'] =NOTIFIER_USERNAME
data_item['notifier']['default']['password'] =NOTIFIER_PASSWORD
data_item['notifier']['default']['group-whitelist'] =NOTIFIER_GROUP_WHITELIST

#with open('burrow.json') as data_file:
#    data_item = json.load(data_file)
#set zookeeper servers
zk = os.environ['ZK']
data_item['zookeeper']['servers'] = list(zk1.split(','))
#set brokers servers
brokers = os.environ['BROKERS']
data_item['cluster']['local']['servers'] = list(brokers.split(','))
data_item['consumer']['local']['servers'] = list(brokers.split(','))
#set sasl username and password(actually token)
username = os.environ['USERNAME']
password = os.environ['TOKEN']
data_item['sasl']['saslprofile']['username']=username
data_item['sasl']['saslprofile']['password']=password

print(data_item['zookeeper']['servers'])

with open('burrow.toml', 'w') as outfile:
    toml.dump(data_item, outfile)

    print(data_item)