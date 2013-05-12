#!/usr/bin/env python

import esclient

class UserLogFetcher:
    def __init__(self, esurl="http://localhost:9200"):
        self._es = esclient.ESClient(esurl)

    def get_userlog(self, uid):
        messages = []
        qbody = {
                "query": {
                    "term" : { "uid" : uid }
                }
            }
    
        result = self._es.search(query_body=qbody)
        result = result["hits"]["hits"]
        for log in result:
            data = log['_source']['@fields']
            messages.append((data['timestamp'], data['data']))

        return messages

if __name__ == '__main__':
    ulog = UserLogFetcher('http://172.16.21.139:9200')
    for uid in [123, 103]:
        print "Userlogs for uid", uid
        for i in ulog.get_userlog(uid):
            print i



