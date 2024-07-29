from django.shortcuts import render
from app01 import models

# Create your views here.

'部门列表'
def depart_list(request):

    # 去数据库中获取所有的部门列表
    # [对象,对象,对象]
    queryset = models.Department.objects.all()

    return render(request,'depart_list.html',{'queryset':queryset})
