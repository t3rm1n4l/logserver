from django.shortcuts import render_to_response
from logserverui.lib.userlog import UserLogFetcher
from django.conf import settings
from requests import ConnectionError

page_limit = settings.UI_PAGE_LIMIT

def index(request):
    uid = 0
    page = 0
    hours = 0
    error = None

    current_uid = "user id"
    current_hours = "hours"

    if request.GET.has_key('uid'):
        try:
            uid = int(request.GET['uid'])
        except:
            error = "Invalid uid"

    if request.GET.has_key('page'):
        try:
            page = int(request.GET['page'])
        except:
            error = "Invalid page"

    if request.GET.has_key('hours'):
        try:
            hours = int(request.GET['hours'])
        except:
            error = "Invalid hours"

    if uid:
        current_uid = "%d" %uid

    if hours:
        current_hours = "%d" %hours

    ufetcher = UserLogFetcher(settings.ELASTICSEARCH_URL)

    try:
        count, messages = ufetcher.get_userlog(uid, hours, page*page_limit, page_limit)
    except ConnectionError,e:
        error = "Unable to reach elasticsearch server"

    if error:
        return render_to_response('index.html', {"error": error})

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


