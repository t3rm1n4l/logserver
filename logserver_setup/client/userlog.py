#!/usr/bin/env python

import esclient
import datetime

def genquery(uid, recent_hrs=0, sort=False, offset=None, size=None):
        qbody = {
                "query": {
                    "filtered" : {
                        "query": {
                            "term" : { "uid" : uid }
                        },
                    },

                }
        }

        #TODO: Add filter by string
        #x = {"filter" : {
        #    "query" : {
        #        "query_string": {
        #            "query" : r'" 1 at Sun"'
        #        }
        #    }
        #}
        #}
        #qbody["query"]["filtered"].update(x)

        if recent_hrs:
            timestamp = datetime.datetime.now() - datetime.timedelta(hours=recent_hrs)
            print timestamp.strftime("%Y-%m-%dT%H:%M:%S")

            timefilter = {
                    "filter" : {
                        "range" : {
                            "@timestamp" : {
                                "from" : timestamp.strftime("%Y-%m-%dT%H:%M:%S")
                                }
                        }
                    }
            }

            qbody["query"]["filtered"].update(timefilter)

        if offset:
            qbody["from"] = offset

        if size:
            qbody["size"] = size

        if sort:
            qbody["sort"] = [
                    {"@timestamp" : "desc"},
            ]

        return qbody


class UserLogFetcher:
    def __init__(self, esurl="http://localhost:9200"):
        self._es = esclient.ESClient(esurl)

    def get_userlog(self, uid, hours=0, offset=None, size=None):
        messages = []
        query = genquery(uid, hours, True, offset, size)
        result = self._es.search(query_body=query)
        total = result['hits']['total']
        result = result["hits"]["hits"]
        for log in result:
            data = log['_source']['@fields']
            messages.append((data['timestamp'][0], data['data'][0]))

        return total, messages

if __name__ == '__main__':
    ulog = UserLogFetcher('http://172.16.21.139:9200')
    for uid in [123, 103]:
        count, msgs = ulog.get_userlog(uid)
        print "Userlogs for uid %d and count is %d" %(uid, count)
        for i in msgs:
            print i



