from django.shortcuts import render, HttpResponse, redirect
from django import forms
from app01 import models
from app01.utils.encrypt import md5
from app01.utils.bootstrap import BootStrapForm

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
    )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

'登录'
def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        return redirect("/admin/list/")

    return render(request, 'login.html', {'form': form})

