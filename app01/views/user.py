from django.shortcuts import render,redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm,PrettyNumModelForm,PrettyNumEditModelForm
# Create your views here.

'用户管理'
def user_list(request):
    # 获取所有用户列表
    queryset = models.UserInfo.objects.all()
    page_object = Pagination(request,queryset,page_size=10)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
    }
    return render(request,'user_list.html',context)

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

'编辑用户'
def user_edit(request,nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据
        form = UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{'form':form})

    form = UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request,'user_edit.html',{'form':form})

'删除用户'
def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
