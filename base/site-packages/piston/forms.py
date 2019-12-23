import hmac, base64

from django import forms
from django.conf import settings

class Form(forms.Form):
    pass
    
class ModelForm(forms.ModelForm):
    """
    Subclass of `forms.ModelForm` which makes sure
    that the initial values are present in the form
    data, so you don't have to send all old values
    for the form to actually validate. Django does not
    do this on its own, which is really annoying.
    """
    def merge_from_initial(self):
        self.data._mutable = True
        filt = lambda v: v not in self.data.keys()
        for field in filter(filt, getattr(self.Meta, 'fields', ())):
            self.data[field] = self.initial.get(field, None)


class OAuthAuthenticationForm(forms.Form):
    oauth_token = forms.CharField(widget=forms.HiddenInput)
    oauth_callback = forms.CharField(widget=forms.HiddenInput, required=False)
    authorize_access = forms.BooleanField(required=True)
    csrf_signature = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)

        self.fields['csrf_signature'].initial = self.initial_csrf_signature

    def clean_csrf_signature(self):
        sig = self.cleaned_data['csrf_signature']
        token = self.cleaned_data['oauth_token']

        sig1 = OAuthAuthenticationForm.get_csrf_signature(settings.SECRET_KEY, token)

        if sig != sig1:
            raise forms.ValidationError("CSRF signature is not valid")

        return sig

    def initial_csrf_signature(self):
        token = self.initial['oauth_token']
        return OAuthAuthenticationForm.get_csrf_signature(settings.SECRET_KEY, token)

    @staticmethod
    def get_csrf_signature(key, token):
        # Check signature...
        try:
            import hashlib # 2.5
            hashed = hmac.new(key, token, hashlib.sha1)
        except:
            import sha # deprecated
            hashed = hmac.new(key, token, sha)

        # calculate the digest base 64
        return base64.b64encode(hashed.digest())

