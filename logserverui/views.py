from django.http import HttpResponse
from django.shortcuts import render_to_response
from logserverui.lib.userlog import UserLogFetcher

page_limit = 5

def index(request):
    uid = 0
    page = 0
    hours = 0

    current_uid = "user id"
    current_hours = "hours"

    if request.GET.has_key('uid'):
        uid = int(request.GET['uid'])

    if request.GET.has_key('page'):
        page = int(request.GET['page'])

    if request.GET.has_key('hours'):
        hours = int(request.GET['hours'])

    if uid:
        current_uid = "%d" %uid

    if hours:
        current_hours = "%d" %hours

    ufetcher = UserLogFetcher('http://172.16.21.139:9200')
    count, messages = ufetcher.get_userlog(uid, hours, page*page_limit, page_limit)

    maxpages = count/page_limit
    if count % page_limit:
        maxpages += 1
    pages = []

    for i in xrange(maxpages):
        enable_str = "enabled"
        if page == i:
            enable_str = "disabled"

        pages.append((i+1, "?uid=%d&hours=%d&page=%d" %(uid, hours, i), enable_str))

    params = {
    "messages" : messages,
    "pages" : pages,
    }

    if uid:
        params["uid"] =  current_uid

    if hours:
        params["hours"] = current_hours

    return render_to_response('index.html', params)


