Logserver
=========
This is a helper project to setup a log collection server using opensource tools.
Logstash and elasticsearch are two powerful tools that can be combined together to build a highly scalable log indexing and search tool. Logstash can receive logs from many sources such as rsyslog, redis, etc and is able write output in different formats. Elasticsearch is used for text indexing.

## Platform
Ubuntu 13.04


## Installation
    cd logserver_setup
    # ./install.sh

The installer will install the following tools:

1. redis-server
2. elasticsearch
3. logstash
4. kibana ui

## User log console
A django userlog search console is available at django_ui directory.

    cd django_ui
    # Update ELASTICSEARCH_URL in settings.py
    python manage.py runserver


## Testing
    cd logserver_setup/client
    ./testlogger.sh
    ./userlog.py


## Notes
The rsyslog rules setup by the installer script will redirect any log messages containing the text 'myservice' to logstash port 5544. The logstash expects the log messages to have an identifier string 'userid:$uid' in it. It parses the uid and converts to json by removing the uid and attaching a field uid. Logstash sends this message to elasticsearch cluster. Since we have added a tag uid, those messages can be searched easily by using @fields.uid attribute.

The django-ui executes rest api calls to retreive logs for a uid for the past X hours and displays it.

### Work flow
 rsyslog sending log from multiple sources =>  [Logstash reader] => [redis queue]  => [ Logstash indexer ] =>  (Elastic Search Cluster) => Kibana UI

