#!/bin/bash

if [ $UID -ne 0 ];
then 
    echo Please run as root
    exit 1
fi

apt-get install redis-server -y
service redis-server start

sudo apt-get install openjdk-7-jre-headless -y

wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.20.6.deb
dpkg -i elasticsearch-0.20.6.deb

cp elasticsearch.yml /etc/elasticsearch/
service elasticsearch restart

apt-get install libapache2-mod-passenger apache2 ruby ruby1.8-dev libopenssl-ruby rubygems git -y
(
cd /var/www
git clone --branch=kibana-ruby https://github.com/rashidkpc/Kibana.git --depth=1 kibana
cd kibana
gem install bundler
bundle install
)

cp kibanavirthost.conf /etc/apache2/conf.d/
service apache2 restart

cp myservice_syslog.conf /etc/rsyslog.d/
service rsyslog restart

apt-get install default-jre -y
(
cd logstash
wget https://logstash.objects.dreamhost.com/release/logstash-1.1.10-flatjar.jar -O logstash.jar
./logstash_syslogd start
./logstash_indexerd start
)

apt-get install python-requests -y
git clone https://github.com/eriky/ESClient.git
cd ESClient
python setup.py install

