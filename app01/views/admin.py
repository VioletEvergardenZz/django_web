from django.shortcuts import render,redirect
from app01 import models
from app01.utils.pagination import Pagination
from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5

'管理员列表'
def admin_list(request):
    # 搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request,queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string' : page_object.html(),
        'search_data' : search_data,
    }
    return render(request,'admin_list.html',context)

class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = models.Admin
        fields = ['username','password','confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致,请重新输入")
        return confirm
'添加管理员'
def admin_add(request):
    title = '添加管理员'
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request,'change.html',{'form':form,'title':"添加管理员"})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request,'change.html',{'form':form,'title':title})