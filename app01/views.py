from django.shortcuts import render,redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

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

'靓号列表'
def pretty_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    #1. 根据用户想要访问的页码 计算出起止位置
    page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')[start:end]

    # 数据总条数
    total_count = models.PrettyNum.objects.filter(**data_dict).order_by('-level').count()
    # 总页码
    total_page_count,div = divmod(total_count, page_size)
    if div:
        total_page_count += 1

    # 计算当前页的前五页和后五页
    plus = 5
    if total_page_count <= 2* plus + 1:
        start_page = 1
        end_page = total_page_count
    else:
        # 数据库中数据较多 > 11 页
        # 当前页 < 5 时
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            # 当前页 > 5
            # 当前页 + 5 > 总页面
            if (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus
    # 页码
    page_str_list =[]
    # 首页
    page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page-1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    # 页面
    for i in range(start_page,end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i,i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 下一页
    if page < total_page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    page_str_list.append(prev)
    # 尾页
    page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))

    page_string = mark_safe("".join(page_str_list))

    return render(request,'pretty_list.html',{'queryset':queryset,"search_data":search_data,"page_string":page_string})

class PrettyNumModelForm(forms.ModelForm):
    # 验证:方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')]
    )
    class Meta:
        model = models.PrettyNum
        # fields = '__all__'
        fields = ['mobile','price','level','status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有的插件 添加了 class ='form-control'
        for name,field in self.fields.items():
            field.widget.attrs = {'class':'form-control','placeholder':field.label}

    # 验证:方式二
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

'添加靓号'
def pretty_add(request):
    if request.method == "GET":
        form = PrettyNumModelForm()
        return render(request,'pretty_add.html',{'form':form})
    form = PrettyNumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request,'pretty_add.html',{'form':form})


class PrettyNumEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True,label="手机号")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )
    class Meta:
        model = models.PrettyNum
        fields = ['mobile','price','level','status']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # 循环找到所有的插件 添加了 class ='form-control'
        for name,field in self.fields.items():
            field.widget.attrs = {'class':'form-control','placeholder':field.label}
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id = self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

'编辑靓号'
def pretty_edit(request,nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyNumEditModelForm(instance=row_object)
        return render(request,'pretty_edit.html',{'form':form})
    form = PrettyNumEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request,'pretty_edit.html',{'form':form})

'删除靓号'
def pretty_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')

