from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from .models import MyModel
from django.forms import ModelForm


User= get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    #password= forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1','password2')






class MyModelForm(ModelForm):
    class Meta:
        model = MyModel
        fields = ['state']

    def clean(self, *args, **kwargs):
        cleaned_data =super(MyModelForm,self).clean()
        state=cleaned_data.get('state')

class UserInput(forms.Form):
    name=forms.CharField(max_length=30)

    def clean(self):
        cleaned_data=super(UserInput,self).clean()
        name=cleaned_data.get('name')

        if not name:
            raise forms.ValidationError('Enter valid place name!')

class ContactForm(forms.Form):
    name=forms.CharField(max_length=30)

    def clean(self):
        cleaned_data=super(ContactForm,self).clean()
        name=cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("please fill...")

class ValuesForm(forms.Form):
    name1=forms.CharField(max_length=30)
    name2 = forms.CharField(max_length=30)
    name3 = forms.CharField(max_length=30)
    def clean(self):
        cleaned_data=super(ValuesForm,self).clean()
        name1=cleaned_data.get('name1')
        name2 = cleaned_data.get('name2')
        name3 = cleaned_data.get('name3')
        if not name1 or not name2 or not name3:
            raise forms.ValidationError("please fill...")


class RateSubmitForm(forms.Form):
    name1=forms.CharField(max_length=30)
    name2 = forms.CharField(max_length=30)
    name3 = forms.CharField(max_length=30)
    def clean(self):
        cleaned_data=super(RateSubmitForm,self).clean()
        name1=cleaned_data.get('name1')
        name2 = cleaned_data.get('name2')
        name3 = cleaned_data.get('name3')
        if not name1 or not name2 or not name3:
            raise forms.ValidationError("please fill...")
        if float(name3) >5 or float(name3)<1 :
            raise forms.ValidationError("Rate on scale of 1 to 5..")
class ImgForm(forms.Form):
    name=forms.CharField(max_length=30)
    name1 = forms.CharField(max_length=30)
    def clean(self):
        cleaned_data=super(ImgForm,self).clean()
        name=cleaned_data.get('name')
        name1 = cleaned_data.get('name1')

        if not name:
            raise forms.ValidationError("please fill...")