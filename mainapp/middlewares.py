from django.db import connection
import django.utils
from datetime import date, timedelta, datetime
import sys
from mainapp.models import Hits
import httpagentparser


class HitcounterMiddleare(object):

    def process_request(self, request):
        address = request.META['REMOTE_ADDR']
        user_agent = request.META['HTTP_USER_AGENT']
        # print >> sys.stderr,
        (os, browser) = httpagentparser.simple_detect(user_agent)
        d = django.utils.timezone.now() - timedelta(days=1)
        recent_hit = Hits.objects.filter(time__gt=d, ip=address, user_agent=user_agent)
        if recent_hit:
            print >>sys.stderr, "RECENT" + str(recent_hit[0])
        else:
            newhit = Hits(time=django.utils.timezone.now(), ip=address, user_agent=user_agent, os=os, browser=browser)
            newhit.save()
        return None