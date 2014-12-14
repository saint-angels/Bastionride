from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from mainapp.forms import FeedbackForm, RadioVoteForm, RegistrationForm, FeedbackEditForm
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
import xml.etree.ElementTree as ET
import xlwt
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return feedback(request)
            else:
                return HttpResponse('Your account is disabled')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse('Invalid login and/or password')
    else:
        return render(request, 'main_site/login.html')

@login_required
def user_logout(request):
    logout(request)
    return feedback(request)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = RegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = RegistrationForm()
    return render(request, 'main_site/register.html', {'user_form': user_form, 'registered': registered})


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


def question_info_as_xml(request, question_id):
    root = ET.Element("question")
    question = get_object_or_404(Question, pk=question_id)
    name_tag = ET.SubElement(root, "question_text")
    name_tag.text = question.question_text
    choices_tag = ET.SubElement(root, "choices")
    for choice in question.choice_set.all():
        choice_tag = ET.SubElement(choices_tag, "choice")
        choice_text_tag = ET.SubElement(choice_tag, "choice_text")
        choice_text_tag.text = choice.choice_text
        votes_tag = ET.SubElement(choice_tag, "votes")
        votes_tag.text = str(choice.votes)
    tree = ET.ElementTree(root)
    return HttpResponse(ET.tostring(tree.getroot(), encoding='utf8', method='xml'), content_type="text/xml")


def xls_to_response(xls, fname):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname

    xls.save(response)
    return response


def question_info_as_xls(request, question_id):
    workbook = xlwt.Workbook()
    main_sheet = workbook.add_sheet("main sheet")
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all()
    main_sheet.write(0, 0, question.question_text)
    for choice_idx in range(1, len(choices) + 1):
        main_sheet.write(choice_idx, 0, choices[choice_idx - 1].choice_text) # row, column, value
        main_sheet.write(choice_idx, 1, choices[choice_idx - 1].votes)
    return xls_to_response(workbook, 'question_stat.xls')


def feedback(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_html = BeautifulSoup(form.cleaned_data['user_feedback']).prettify()
            x = xssescape.XssCleaner()
            clear_html = x.strip(feedback_html)
            new_feedback = FeedbackMessages(time=timezone.localtime(timezone.now()), text=clear_html, user=request.user)
            new_feedback.save()
            return HttpResponseRedirect('/feedback/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()

    user_id = None
    if request.user.is_authenticated():
        user_id = request.user.id

    feedback_messages = FeedbackMessages.objects.filter(feedbackmessages=None).order_by('-time')
    return render(request, 'main_site/feedback.html', {'feedback_messages': feedback_messages, 'form': form, 'feedback_edit_form': FeedbackEditForm(), 'user_id':user_id})


def feedback_versions(request):
    users = User.objects.all()
    feedback_versions_dict = {}
    for user in users:
        feedback_versions_dict[user.username] = FeedbackMessages.objects.filter(user=user).order_by('-time')

    print feedback_versions_dict
    return render(request, 'main_site/feedback_versions.html', {'user_feedback': feedback_versions_dict})


def edit_feeedback_with_id(request, feedback_id):
    old_feedback = FeedbackMessages.objects.get(id=feedback_id)
    if request.user.is_authenticated() and request.user == old_feedback.user:
        if request.method == 'POST':
            form = FeedbackEditForm(request.POST)
            if form.is_valid():
                feedback_html = BeautifulSoup(form.cleaned_data['user_feedback']).prettify()
                x = xssescape.XssCleaner()
                clear_html = x.strip(feedback_html)
                new_feedback = FeedbackMessages(time=timezone.localtime(timezone.now()), text=clear_html, user=request.user, previous_version=old_feedback)
                new_feedback.save()
                return HttpResponseRedirect('/feedback/')
    user_id = None
    if request.user.is_authenticated():
        user_id = request.user.id

    feedback_messages = FeedbackMessages.objects.filter(feedbackmessages=None).order_by('-time')
    return render(request, 'main_site/feedback.html', {'feedback_messages': feedback_messages, 'form': FeedbackForm(), 'feedback_edit_form': FeedbackEditForm(), 'user_id':user_id})



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