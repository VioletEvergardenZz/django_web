from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=2,
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","gender","depart"]

class PrettyNumModelForm(BootStrapModelForm):
    # 验证:方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')]
    )
    class Meta:
        model = models.PrettyNum
        # fields = '__all__'
        fields = ['mobile','price','level','status']

    # 验证:方式二
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

class PrettyNumEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True,label="手机号")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )
    class Meta:
        model = models.PrettyNum
        fields = ['mobile','price','level','status']
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id = self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile