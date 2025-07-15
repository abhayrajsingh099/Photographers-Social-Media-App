from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']



class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','first_name']


    # use clean_<fields>  to call these methods automatically ( convention )
    def clean_password2(self): #This method gets automatically called during form.is_valid() — you don’t need to call it manually.
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        
        if password!= password2:
            raise forms.ValidationError('Passwords do not match')
        

        # if len(password2)<8: 
        #     raise forms.ValidationError("Password must be at least 8 characters long !")
        
        validate_password(password2) #inbuilt password validator,# Built-in Django strength validator

        return password2
    

