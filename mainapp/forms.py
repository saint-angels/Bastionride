from django import forms
from captcha.fields import CaptchaField


class FeedbackForm(forms.Form):
    user_feedback = forms.CharField(label='Gimme some text',
                                    max_length=500,
                                    widget=forms.Textarea)
    captcha = CaptchaField()