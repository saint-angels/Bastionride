from django import forms
from captcha.fields import CaptchaField
from mainapp.models import Question


class FeedbackForm(forms.Form):
    user_feedback = forms.CharField(label='Gimme some text',
                                    max_length=500,
                                    widget=forms.Textarea)
    captcha = CaptchaField()


class RadioVoteForm(forms.ModelForm):
    captcha = CaptchaField()
    question_text = forms.CharField(required=False)
    selection_type = forms.CharField(required=False)

    class Meta:
        model = Question
        fields = ['question_text', 'selection_type']