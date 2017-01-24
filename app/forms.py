# -*- coding: utf-8 -*-

"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from app.models import Student, StudentGroup


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form which uses bootstrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': u'email'}))
    password = forms.CharField(label=_(u"Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': u'password'}))


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    A custom form that lets a user change their password by entering their old
    password.
    """
    old_password = forms.CharField(label=_(u"current password"),
                                   widget=forms.PasswordInput(
                                       {
                                           'class': 'form-control',
                                           'placeholder': u'current password'
                                       }
                                   ))
    new_password1 = forms.CharField(label=_(u"New password"),
                                    widget=forms.PasswordInput(
                                        {
                                            'class': 'form-control',
                                            'placeholder': u'new password'
                                        }
                                    ))
    new_password2 = forms.CharField(label=_(u"Confirm new password"),
                                    widget=forms.PasswordInput(
                                        {
                                            'class': 'form-control',
                                            'placeholder': u'confirm new '
                                                           u'password'
                                        }
                                    ))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
        )


class NewUserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = (
            'user',
        )

    _attrs = {
        'class': 'form-control',
    }

    first_name = forms.CharField(widget=forms.TextInput(_attrs))
    middle_name = forms.CharField(widget=forms.TextInput(_attrs))
    last_name = forms.CharField(widget=forms.TextInput(_attrs))
    stud_id = forms.CharField(widget=forms.TextInput(_attrs))


class NewGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = ['name']

    name = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
    }))
