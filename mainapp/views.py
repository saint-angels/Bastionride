from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from mainapp.forms import FeedbackForm, RadioVoteForm
from mainapp.models import FeedbackMessages, Hits, Question, Choice
import django.utils
from django.utils import formats, timezone
from datetime import timedelta
from PIL import Image, ImageDraw
import httpagentparser
from BeautifulSoup import BeautifulSoup
import xssescape
import sys
import json
import base64
import cStringIO
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def index(request):
    return render(request, 'main_site/index.html', {})


def about(request):
    return render(request, 'main_site/about.html', {})


def gallery(request):
    return render(request, 'main_site/gallery.html', {})


def polls(request):
    question_list = Question.objects.order_by('-pub_date')
    question_forms = []
    for question in question_list:
        question_forms.append(RadioVoteForm(instance=question))

    return render(request, 'main_site/polls.html', {'question_forms': question_forms})


# def vote(request, question_id):
#
#     if request.method == 'POST':
#         form = RadioVoteForm(request.POST)
#         if form.is_valid():
#             p = get_object_or_404(Question, pk=question_id)
#             try:
#                 selected_choice = p.choice_set.get(pk=request.POST['choice'])
#             except (KeyError, Choice.DoesNotExist):
#                 # print >>sys.stderr, 'VOTE FORM ERROR: ' + request.POST['choice']
#                 return render(request, 'main_site/polls.html', {
#                     'questions': Question.objects.order_by('-pub_date'),
#                     'error_message': "You didn't select a choice.",
#                 })
#             else:
#                 selected_choice.votes += 1
#                 selected_choice.save()
#         else:
#             print >>sys.stderr, 'VOTE FORM ERROR: ' + str(form.errors)
#
#     # This prevents data from being posted twice if user hits the Back button
#     return HttpResponseRedirect(reverse('polls'))
def vote(request, question_id):

    response_json = {}
    if request.method == 'POST':
        form = RadioVoteForm(request.POST)
        if form.is_valid():
            p = get_object_or_404(Question, pk=question_id)
            try:
                selected_choice = p.choice_set.get(pk=request.POST['choice'])
            except (KeyError, Choice.DoesNotExist):
                response_json['error'] = "You didn't select a choice."
            else:
                selected_choice.votes += 1
                selected_choice.save()
                response_json['status'] = 1
                response_json['new_cptch_key'] = CaptchaStore.generate_key()
                response_json['new_cptch_image'] = captcha_image_url(response_json['new_cptch_key'])
        else:
            response_json['status'] = 0
            response_json['form_errors'] = form.errors
            response_json['new_cptch_key'] = CaptchaStore.generate_key()
            response_json['new_cptch_image'] = captcha_image_url(response_json['new_cptch_key'])
            print >>sys.stderr, 'VOTE FORM ERROR: ' + str(form.errors)
    else:
        response_json['error'] = "Method is not POST"
    return HttpResponse(json.dumps(response_json), content_type="application/json")


def question_info_image(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    lines_to_render = []
    for choice in question.choice_set.all():
        lines_to_render.append(choice.choice_text + ": " + str(choice.votes))
    size = (200, len(lines_to_render) * 15)
    im = Image.new('RGB', size, (25, 25, 25))
    draw = ImageDraw.Draw(im)
    for lineIdx in range(0, len(lines_to_render)):
        text_pos = (0, 12 * lineIdx)
        draw.text(text_pos, lines_to_render[lineIdx], (255, 255, 255))
    del draw
    response = HttpResponse(content_type="image/png")
    im.save(response, 'PNG')
    return response


def question_info_image_b64(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    lines_to_render = []
    for choice in question.choice_set.all():
        lines_to_render.append(choice.choice_text + ": " + str(choice.votes))
    size = (200, len(lines_to_render) * 15)
    im = Image.new('RGB', size, (25, 25, 25))
    draw = ImageDraw.Draw(im)
    for lineIdx in range(0, len(lines_to_render)):
        text_pos = (0, 12 * lineIdx)
        draw.text(text_pos, lines_to_render[lineIdx], (255, 255, 255))
    del draw

    jpeg_image_buffer = cStringIO.StringIO()
    im.save(jpeg_image_buffer, format="PNG")
    imgStr = base64.b64encode(jpeg_image_buffer.getvalue())
    return HttpResponse(imgStr)


def feedback(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_html = BeautifulSoup(form.cleaned_data['user_feedback']).prettify()
            x = xssescape.XssCleaner()
            clear_html = x.strip(feedback_html)
            new_feedback = FeedbackMessages(time=timezone.localtime(timezone.now()), text=clear_html)
            new_feedback.save()
            return HttpResponseRedirect('/feedback/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()

    feedback_messages = FeedbackMessages.objects.all().order_by('-time')
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
    last_visit = Hits.objects.filter(ip=address, user_agent=user_agent).latest()

    (os, browser) = httpagentparser.simple_detect(user_agent)

    lines_to_render = ["All: " + all_hits_count,
                       "Today: " + today_hits_count,
                       "Your last visit: " + formats.date_format(timezone.localtime(last_visit.time), "SHORT_DATETIME_FORMAT"),
                       "Your browser: " + browser]
    white_color = (255, 255, 255)
    for lineIdx in range(0, len(lines_to_render)):
        text_pos = (0, 12 * lineIdx)
        draw.text(text_pos, lines_to_render[lineIdx], white_color)
    del draw

    response = HttpResponse(content_type="image/png")
    im.save(response, 'PNG')
    return response