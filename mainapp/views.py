from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from mainapp.forms import FeedbackForm
from mainapp.models import FeedbackMessages, Hits
import django.utils
from django.utils import formats
from datetime import timedelta
from PIL import Image, ImageDraw
from datetime import datetime
import sys
import httpagentparser


def index(request):
    return render(request, 'main_site/index.html', {})


def about(request):
    return render(request, 'main_site/about.html', {})


def gallery(request):
    return render(request, 'main_site/gallery.html', {})


def feedback(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print >> sys.stderr, "FORM" + keeptags(form.cleaned_data['user_feedback'], 'B I IMG b i img')
            feedbackText = keeptags(form.cleaned_data['user_feedback'], 'B I IMG b i img')
            newFeedback = FeedbackMessages(time=django.utils.timezone.now(), text=feedbackText)
            newFeedback.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/feedback/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()

    feedback_messages = FeedbackMessages.objects.all()
    return render(request, 'main_site/feedback.html', {'form': form, 'feedback_messages': feedback_messages})


def hitcount_image(request):
    size = (250, 50)
    im = Image.new('RGB', size, (25, 25, 25))
    draw = ImageDraw.Draw(im)   # create a drawing object that is
                                # used to draw on the new image
    all_hits_count = str(Hits.objects.count())

    a_day_ago = django.utils.timezone.now() - timedelta(days=1)
    today_hits_count = str(Hits.objects.filter(time__gt=a_day_ago).count())


    address = request.META['REMOTE_ADDR']
    user_agent = request.META['HTTP_USER_AGENT']
    lastVisit = Hits.objects.filter(ip=address, user_agent=user_agent).latest()

    (os, browser) = httpagentparser.simple_detect(user_agent)

    lines_to_render = ["All: " + all_hits_count,
                       "Today: " + today_hits_count,
                       "Your last visit: " + formats.date_format(lastVisit.time, "SHORT_DATETIME_FORMAT"),
                       "Your browser: " + browser]
    white_color = (255, 255, 255)
    for lineIdx in range(0, len(lines_to_render)):
        text_pos = (0, 12 * lineIdx)
        draw.text(text_pos, lines_to_render[lineIdx], white_color)
    del draw

    response = HttpResponse(content_type="image/png")
    im.save(response, 'PNG')
    return response


def keeptags(value, tags):
    """
    Strips all [X]HTML tags except the space seperated list of tags
    from the output.

    Usage: keeptags:"strong em ul li"
    """
    import re
    from django.utils.html import strip_tags, escape
    tags = [re.escape(tag) for tag in tags.split()]
    tags_re = '(%s)' % '|'.join(tags)
    singletag_re = re.compile(r'<(%s\s*/?)>' % tags_re)
    starttag_re = re.compile(r'<(%s)(\s+[^>]+)>' % tags_re)
    endtag_re = re.compile(r'<(/%s)>' % tags_re)
    value = singletag_re.sub('##~~~\g<1>~~~##', value)
    value = starttag_re.sub('##~~~\g<1>\g<3>~~~##', value)
    value = endtag_re.sub('##~~~\g<1>~~~##', value)
    value = strip_tags(value)
    value = escape(value)
    recreate_re = re.compile('##~~~([^~]+)~~~##')
    value = recreate_re.sub('<\g<1>>', value)
    return value