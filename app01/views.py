from django.shortcuts import render,redirect
from app01 import models
from django import forms

# Create your views here.

'部门列表'
def depart_list(request):
    # 去数据库中获取所有的部门列表
    # [对象,对象,对象]
    queryset = models.Department.objects.all()
    return render(request,'depart_list.html',{'queryset':queryset})

'添加部门'
def depart_add(request):
    if request.method == "GET":
        return render(request,'depart_add.html')

    # 获取用户POST提交过来的数据
    title = request.POST.get('title')
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回部门列表
    return redirect('/depart/list/')

'删除部门'
def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')

'修改部门'
def depart_edit(request,nid):
    if request.method == "GET":
        # 根据nid 获取它的数据
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request,'depart_edit.html',{'row_object':row_object})

    # 获取用户提交的标题
    title = request.POST.get('title')
    # 根据id 找到数据库中的数据并进行更新
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')

'用户管理'
def user_list(request):
    # 获取所有用户列表
    queryset = models.UserInfo.objects.all()
    return render(request,'user_list.html',{'queryset':queryset})

'添加用户'
def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choices' : models.UserInfo.gender_choices,
            'depart_list' : models.Department.objects.all()
        }
        return render(request,'user_add.html',context)
    # 获取用户提交数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender = request.POST.get('gd')
    depart_id = request.POST.get('dp')

    # 添加到数据库
    models.UserInfo.objects.create(name=user,password=pwd,age=age,account=account,
                                   create_time=ctime,gender=gender,depart_id=depart_id)

    return redirect('/user/list/')


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2,label="用户名")
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","gender","depart"]
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有的插件 添加了 class ='form-control'
        for name,field in self.fields.items():
            field.widget.attrs = {'class':'form-control','placeholder':field.label}

'添加用户(ModelForm)'
def user_model_form_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request,'user_model_form_add.html',{'form':form})
    # 用户POST提交数据,数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法,保存到数据库
        form.save()
        return redirect('/user/list/')
    # 校验失败 (在页面上显示错误信息)
    return render(request,'user_model_form_add.html',{'form':form})
