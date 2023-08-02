from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='username',max_length=32)
    email = models.EmailField(verbose_name='email',max_length=32)
    mobile_phone = models.CharField(verbose_name='mobile phone',max_length=32)
    password = models.CharField(verbose_name='password',max_length=32)

    #price_stategy = models.ForeignKey(verbose_name='price_strategy',to='PriceStrategy',null=True,blank=True)

class PriceStrategy(models.Model):
    category_choices=(
        (1,'Free'),
        (2,'VIP'),
        (3,'SVIP'),
        (4,'other')
    )
    category = models.SmallIntegerField(verbose_name='Charge Category',default=1,choices=category_choices)
    title = models.CharField(verbose_name='Title',max_length=32)
    price = models.PositiveIntegerField(verbose_name='Price')

    project_num = models.PositiveIntegerField(verbose_name='Max Project Number')
    project_mem = models.PositiveIntegerField(verbose_name='Max Project Member')
    project_space = models.PositiveIntegerField(verbose_name='Project Space',help_text='G')
    per_file_size = models.PositiveIntegerField(verbose_name='Per file size (M)',help_text='M')

    create_datetime = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
class Transaction(models.Model):
    status_choices =(
        (1,'Paid'),
        (2,'unpaid')
    )
    status = models.SmallIntegerField(verbose_name='status',choices=status_choices,default=2)
    userId = models.ForeignKey(verbose_name='user',to='UserInfo',on_delete=models.CASCADE)
    price_strategy = models.ForeignKey(verbose_name='Price Policy',to='PriceStrategy')
    paidAmt = models.IntegerField(verbose_name='Actual payment',default=0)
    startTime = models.DateTimeField(verbose_name='Package Valid from',null=True,blank=True)
    validUntil = models.DateTimeField(verbose_name='Package Valid Until',null=True,blank=True)
    amtYear = models.IntegerField(verbose_name='Purchased Years',default=0)
    orderId = models.CharField(verbose_name='Order No.',max_length=64,unique=True)
    create_datetime = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)

class Project(models.Model):
    color_choices = (
        (1, "#56b8eb"),
        (2, "#f28033"),
        (3, "#ebc656"),
        (4, "#a2d148"),
        (5, "#20BFA4"),
        (6, "#7461c2"),
        (7, "#20bfa3"),

    )
    name = models.CharField(verbose_name='Project Name',max_length=32)
    description = models.CharField(verbose_name='Project Description',max_length=255,null=True,blank=True)
    color = models.SmallIntegerField(verbose_name='Color',choices=color_choices,default=1)
    use_space = models.IntegerField(verbose_name='Project Used Space',default=0,help_text='Bytes')
    star = models.BooleanField(verbose_name='Star', default=False)

    bucket = models.CharField(verbose_name='cos bucket',max_length=128)
    region = models.CharField(verbose_name='cos bucket region', max_length=32)

    join_count = models.SmallIntegerField(verbose_name='Joined Population',default=1)
    creator = models.ForeignKey(verbose_name='Creator',to='UserInfo')
    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)



    #定义多对多关系，可以方便联表查询。如果没有through会自动建新表。through表示把新表内容放在through关联的表里。好处是关联的表可以定义原本表没有的字段
    #project_user = models.ManyToManyField(to='UserInfo',through='ProjectUser',through_fields=('project','user'))

class ProjectUser(models.Model):
    userId = models.ForeignKey(verbose_name='User',to='UserInfo',on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='Project',to='Project')


    star = models.BooleanField(verbose_name='Star',default=False)
    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)


#wiki
class Wiki(models.Model):
    project = models.ForeignKey(verbose_name='Project',to='Project')
    title = models.CharField(verbose_name='Title',max_length=32)
    content = models.TextField(verbose_name='Content')

    depth=models.IntegerField(verbose_name='level',default=1)
    #实现多级评论，parent字段需要关联上级的ID，所以使用自关联。自关联可以 to='Wiki'也可以to='self'
    #related_name用于反向关联，parent评论找子对象
    parent = models.ForeignKey(verbose_name='Parent File',to='Wiki',null=True,blank=True,related_name='children')
    def __str__(self):
        return self.title

#Files
class Files(models.Model):
    project_id = models.ForeignKey(verbose_name='Project',to='Project')
    FileName = models.CharField(verbose_name='File Name',max_length=32,help_text="Directory/FileName")
    type_choices = (
        (1,'Dir'),
        (2,'Doc')
    )
    type = models.SmallIntegerField(verbose_name='type',choices=type_choices)
    size = models.IntegerField(verbose_name='File Size',null=True,blank=True,help_text='Bytes')

    path = models.CharField(verbose_name='Path',max_length=255,null=True,blank=True)

    parent = models.ForeignKey(verbose_name='Parent File',to='Files',null=True,blank=True,related_name='children')
    key=models.CharField(verbose_name='Key',max_length=128,null=True,blank=True)
    update_user = models.ForeignKey(verbose_name='Update by',to='UserInfo')
    update_datetime = models.DateTimeField(verbose_name='Update At', auto_now=True)