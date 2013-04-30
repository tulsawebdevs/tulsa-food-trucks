from django import forms
from django.core.urlresolvers import reverse

from django_localflavor_us.forms import USPhoneNumberField
from .models import EmailVerification, PhoneVerification, User


# class AuthenticationForm(forms.Form):


# class RegisterForm(forms.ModelForm):
class RegisterForm(forms.Form):
    class Meta:
        model = User
        
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = USPhoneNumberField(required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'There is already a user with that email.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('email')
        if phone and User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                'There is already a user with that phone number.')
        return phone

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data

    def save(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password']
        user = User.objects.create_user(email, password=password, phone=phone,
                                 first_name=first_name, last_name=last_name)
        if phone:
            PhoneVerification.create_with_unique_code(phone)
        EmailVerification.create_with_unique_code(email)
        # user.save()
        return user


class VerifyEmailForm(forms.ModelForm):

    class Meta:
        model = EmailVerification
        fields = ('code',)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            self.instance = EmailVerification.objects.get(code=code)
        except EmailVerification.DoesNotExist:
            raise forms.ValidationError('Unknown code')
        return code

    def save(self):
        assert self.instance
        email = self.instance.value
        self.instance.delete()
        user = User.objects.get(email=email)
        user.profile.email_confirmed = True
        user.profile.save()
        return user


class VerifyPhoneForm(forms.ModelForm):

    class Meta:
        model = PhoneVerification
        fields = ('code',)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            self.instance = PhoneVerification.objects.get(code=code)
        except PhoneVerification.DoesNotExist:
            raise forms.ValidationError('Unknown code')
        return code

    def save(self):
        assert self.instance
        phone = self.instance.value
        self.instance.delete()
        user = User.objects.get(profile__phone=phone)
        user.profile.phone_confirmed = True
        user.profile.save()
        return user