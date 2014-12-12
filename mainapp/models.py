from django.db import models


class Hits(models.Model):
    time = models.DateTimeField()
    ip = models.CharField(max_length=30)
    user_agent = models.TextField()
    os = models.CharField(max_length=40, default='Unknown')
    browser = models.CharField(max_length=40, default='Unknown')

    def __unicode__(self):
        return str(self.time) + " " + self.ip + self.user_agent

    class Meta:
        get_latest_by = "time"


class FeedbackMessages(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __unicode__(self):
        return self.text


SELECTION_TYPES = (
    ('radio', 'Radio button'),
    ('dropdown', 'Drop-down list'),
)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    selection_type = models.CharField(max_length=10, choices=SELECTION_TYPES, default='radio')

    def __unicode__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text