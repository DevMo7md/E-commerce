from typing import Any
from django.contrib.auth.forms import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, SetPasswordForm
from .models import Profile


class UpdateInfoForm(forms.ModelForm):

    phone = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your phone number'}), required=False)
    address1 = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your address'}), required=False)
    address2 = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter another address (optional)'}), required=False) 
    city = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your city'}), required=False)
    state = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your state'}), required=False) 
    country = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your country'}), required=False)
    zip_code = forms.CharField(label= '', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Inter your zip code'}), required=False) 

    class Meta:

        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'country', 'zip_code')


#  <input type="password" class="form-control" placeholder="Inter old password" name="old_password">
class UpdatePwForm(SetPasswordForm):
    class Meta :
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(UpdatePwForm, self).__init__(*args, **kwargs)  

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted small">Enter the same password as before, for verification.</span>'




class UpdateUserForm(UserChangeForm):
    # remove password message 
    '''
    Password:
    No password set.
    Raw passwords are not stored, so there is no way to see this user’s password, but you can change the password using this form.
    '''
    password = None
    email = forms.EmailField(label='', widget=forms.TextInput,)
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('username','first_name', 'email' )

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)  

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class"">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. </span>'
