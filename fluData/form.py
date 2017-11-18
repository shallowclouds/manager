from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model
from .models import House, UserProfile

class AddHouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['name', 'phone', 'price', 'price_unit', 'house_type',
        'ikeys', 'community', 'position', 'area', 'kind', 'more', 'floor',
        'status', 'decor',
        ]
    # name = forms.CharField(max_length=30, required=False)

    # phone = forms.CharField(max_length=20, required=False)

    # price = forms.IntegerField(required=False)

    # price_unit = forms.CharField(max_length=20, required=False)

    # house_type = forms.CharField(max_length=20, required=False)
    # ikeys = forms.CharField(max_length=40, required=False)
    # community = forms.CharField(max_length=50, required=False)
    # position = forms.CharField(max_length=200, required=False)
    # area = forms.IntegerField(required=False)
    # kind = forms.CharField(max_length=50, required=False)
    # more = forms.CharField(max_length=1000, required=False)
    # floor = forms.IntegerField(required=False)
    # status = forms.CharField(max_length=20, required=False)
    # decor = forms.CharField(max_length=50, required=False)



class LoginUserForm(forms.Form):
    username = forms.CharField(label=u'账 号',error_messages={'required':u'账号不能为空'},
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=u'密 码',error_messages={'required':u'密码不能为空'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'原始密码',error_messages={'required':'请输入原始密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label=u'新密码',error_messages={'required':'请输入新密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label=u'重复输入',error_messages={'required':'请重复新输入密码'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(u'原密码错误')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1)<6:
            raise forms.ValidationError(u'密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user
