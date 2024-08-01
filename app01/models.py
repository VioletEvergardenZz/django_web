from django.db import models

# Create your models here.

class XX(models.Model):
    title = models.CharField(verbose_name="名称", max_length=32)
    image = models.FileField(verbose_name="头像", upload_to="avatar/")

'管理员'
class Admin(models.Model):
    username = models.CharField(verbose_name="管理员",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

    def __str__(self):
        return self.username

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

'任务'
class Task(models.Model):
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")

    # user_id
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)

'订单'
class Order(models.Model):
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    # admin_id
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)

'老板'
class Boss(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)

'城市'
class City(models.Model):

    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")

    # 本质上数据库也是CharField，自动保存数据。
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')


