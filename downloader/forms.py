from django import forms

class DownloadForm(forms.Form):
    url = forms.URLField(label="Video URL", widget=forms.URLInput(attrs={
        "class": "form-control",
        "placeholder": "Paste YouTube/TikTok/Instagram link here"
    }))
