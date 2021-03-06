from django import forms
from django.forms import ModelForm
from .models import YouTubeDL


class YouTubeDLForm(ModelForm):
    class Meta:
        model = YouTubeDL
        fields = ['url']


class FormatVideoForm(forms.Form):

    def __init__(self, choices, *args, **kwargs):
        super(FormatVideoForm, self).__init__(*args, **kwargs)
        self.fields['format_video'] = forms.ChoiceField(choices=choices)
        self.fields['format_video'].label = ""
        self.fields['email'] = forms.EmailField()
