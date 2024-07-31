from django.db import models

# Create your models here.


'管理员'
class Admin(models.Model):
    username = models.CharField(verbose_name="管理员",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

'部门表'
class Department(models.Model):
    title = models.CharField(verbose_name='标题',max_length=32)
    def __str__(self):
        return self.title

'员工表'
class UserInfo(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=16)
    password = models.CharField(verbose_name='密码',max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额',max_digits=10,decimal_places=2,default=0)
    # create_time = models.DateTimeField(verbose_name='入职时间')
    create_time = models.DateField(verbose_name='入职时间')
    # depart_id 有约束 级联删除
    depart = models.ForeignKey(verbose_name="部门",to="department",to_field="id",on_delete=models.CASCADE)
    # Django中的约束
    gender_choices = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)

'靓号表'
class PrettyNum(models.Model):
    mobile = models.CharField(verbose_name="手机号",max_length=11)
    price = models.IntegerField(verbose_name="价格",default=0)
    level_choices = ((1,"1星"),(2,"2星"),(3,"3星"),(4,"4星"),(5,"5星"))
    level = models.SmallIntegerField(verbose_name="星级",choices=level_choices,default=1)
    status_choices = ((0,"未使用"),(1,"已占用"))
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choices,default=0)
