from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    my_file = forms.FileField(required=False)
    my_image = forms.ImageField(required=False)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    my_file = forms.FileField(required=False)


class UploadForm(forms.Form):
    """
    上传相关表单
    """
    # my_file = forms.FileField(required=False)
    my_image = forms.ImageField(required=False)
