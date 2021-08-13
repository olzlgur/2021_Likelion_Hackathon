# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.db import models
from .models import Blog, Profile

class CustomUserCreationForm(UserCreationForm):
    # UserCreationForm을 상속받아 CustomUserCreationForm을 만든다.
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "사용자 이름",
        })
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호(8자 이상)",
        })
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder": "비밀번호 확인",
        })
    )
    class Meta:
        model = get_user_model() # 이 폼이 적용될 모델을 지정한다.
        fields = ['username', 'password1', 'password2',]
        # 이 폼에서 입력 받을 필드명을 지정한다.

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name',]
        
class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(label="별명", required=False)
    description = forms.CharField(label="자기소개", required=False, widget=forms.Textarea())
    profile_photo = forms.ImageField(label="이미지", required=False)
   	# 위의 내용을 정의하지 않아도 상관없지만, 화면에 출력될 때 label이 영문으로 출력되는 것이 싫어서 수정한 것이다..
    class Meta:
        model = Profile
        fields = ['nickname', 'description', 'profile_photo',]

class Blog_form(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['author', 'images']