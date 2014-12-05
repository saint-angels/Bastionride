from django import forms


class FeedbackForm(forms.Form):
    user_feedback = forms.CharField(label='Gimme some text', max_length=100)