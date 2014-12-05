from django.db import models


class Hits(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=30)
    user_agent = models.TextField()

    def __unicode__(self):
        return str(self.time) + " " + self.ip + self.user_agent

    class Meta:
        get_latest_by = "time"


class FeedbackMessages(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


