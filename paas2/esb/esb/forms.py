from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    code = forms.CharField()


class EditForm(forms.Form):
    config = forms.CharField()
    code = forms.CharField()


class DeleteForm(forms.Form):
    code = forms.CharField()
