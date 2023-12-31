from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name='username', max_length=32)
    email = models.EmailField(verbose_name='email', max_length=32)
    mobile_phone = models.CharField(verbose_name='mobile phone', max_length=32)
    password = models.CharField(verbose_name='password', max_length=32)

    def __str__(self):
        return self.username

    # price_stategy = models.ForeignKey(verbose_name='price_strategy',to='PriceStrategy',null=True,blank=True)


class PriceStrategy(models.Model):
    category_choices = (
        (1, 'Free'),
        (2, 'VIP'),
        (3, 'SVIP'),
        (4, 'other')
    )
    category = models.SmallIntegerField(verbose_name='Charge Category', default=1, choices=category_choices)
    title = models.CharField(verbose_name='Title', max_length=32)
    price = models.PositiveIntegerField(verbose_name='Price')

    project_num = models.PositiveIntegerField(verbose_name='Max Project Number')
    project_mem = models.PositiveIntegerField(verbose_name='Max Project Member')
    project_space = models.PositiveIntegerField(verbose_name='Project Space', help_text='G')
    per_file_size = models.PositiveIntegerField(verbose_name='Per file size (M)', help_text='M')

    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)


class Transaction(models.Model):
    status_choices = (
        (1, 'Paid'),
        (2, 'unpaid')
    )
    status = models.SmallIntegerField(verbose_name='status', choices=status_choices, default=2)
    userId = models.ForeignKey(verbose_name='user', to='UserInfo', on_delete=models.CASCADE)
    price_strategy = models.ForeignKey(verbose_name='Price Policy', to='PriceStrategy',on_delete=models.CASCADE)
    paidAmt = models.IntegerField(verbose_name='Actual payment', default=0)
    startTime = models.DateTimeField(verbose_name='Package Valid from', null=True, blank=True)
    validUntil = models.DateTimeField(verbose_name='Package Valid Until', null=True, blank=True)
    amtYear = models.IntegerField(verbose_name='Purchased Years', default=0)
    orderId = models.CharField(verbose_name='Order No.', max_length=64, unique=True)
    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)


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
    name = models.CharField(verbose_name='Project Name', max_length=32)
    description = models.CharField(verbose_name='Project Description', max_length=255, null=True, blank=True)
    color = models.SmallIntegerField(verbose_name='Color', choices=color_choices, default=1)
    use_space = models.IntegerField(verbose_name='Project Used Space', default=0, help_text='Bytes')
    star = models.BooleanField(verbose_name='Star', default=False)

    bucket = models.CharField(verbose_name='cos bucket', max_length=128)
    region = models.CharField(verbose_name='cos bucket region', max_length=32)

    join_count = models.SmallIntegerField(verbose_name='Joined Population', default=1)
    creator = models.ForeignKey(verbose_name='Creator', to='UserInfo',on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)

    # 定义多对多关系，可以方便联表查询。如果没有through会自动建新表。through表示把新表内容放在through关联的表里。好处是关联的表可以定义原本表没有的字段
    # project_user = models.ManyToManyField(to='UserInfo',through='ProjectUser',through_fields=('project','user'))


class ProjectUser(models.Model):
    userId = models.ForeignKey(verbose_name='User', to='UserInfo', on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='Project', to='Project',on_delete=models.CASCADE)

    star = models.BooleanField(verbose_name='Star', default=False)
    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)


# wiki
class Wiki(models.Model):
    project = models.ForeignKey(verbose_name='Project', to='Project',on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Title', max_length=32)
    content = models.TextField(verbose_name='Content')

    depth = models.IntegerField(verbose_name='level', default=1)
    # 实现多级评论，parent字段需要关联上级的ID，所以使用自关联。自关联可以 to='Wiki'也可以to='self'
    # related_name用于反向关联，parent评论找子对象
    parent = models.ForeignKey(verbose_name='Parent File', to='Wiki', null=True, blank=True, related_name='children',on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Files
class Files(models.Model):
    project_id = models.ForeignKey(verbose_name='Project', to='Project',on_delete=models.CASCADE)
    FileName = models.CharField(verbose_name='File Name', max_length=32, help_text="Directory/FileName")
    type_choices = (
        (1, 'Dir'),
        (2, 'Doc')
    )
    type = models.SmallIntegerField(verbose_name='type', choices=type_choices)
    size = models.IntegerField(verbose_name='File Size', null=True, blank=True, help_text='Bytes')

    path = models.CharField(verbose_name='Path', max_length=255, null=True, blank=True)

    parent = models.ForeignKey(verbose_name='Parent File', to='Files', null=True, blank=True, related_name='children',on_delete=models.CASCADE)
    key = models.CharField(verbose_name='Key', max_length=128, null=True, blank=True)
    update_user = models.ForeignKey(verbose_name='Update by', to='UserInfo',on_delete=models.CASCADE)
    update_datetime = models.DateTimeField(verbose_name='Update At', auto_now=True)


class Module(models.Model):
    project = models.ForeignKey(verbose_name='Project', to='Project',on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Issue Title', max_length=32)

    def __str__(self):
        return self.title

class IssueType(models.Model):

    color_choices = (
        (1, "#56b8eb"),
        (2, "#f28033"),
        (3, "#ebc656"),
        (4, "#a2d148"),
        (5, "#20BFA4"),
        (6, "#7461c2"),
        (7, "#20bfa3"),

    )
    PROJECT_INIT_LIST = ["Task", 'Function', 'Bug']
    title = models.CharField(verbose_name='Issue Type', max_length=32)
    color = models.SmallIntegerField(verbose_name='color', choices=color_choices, default=1)
    project = models.ForeignKey(verbose_name='Project', to='Project',on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Issues(models.Model):
    project = models.ForeignKey(verbose_name='Project', to='Project',on_delete=models.CASCADE)
    issues_type = models.ForeignKey(verbose_name='Issue Type', to='IssueType',on_delete=models.CASCADE)
    module = models.ForeignKey(verbose_name='Module', to='Module',null=True,blank=True,on_delete=models.CASCADE)

    subject = models.CharField(verbose_name='subject', max_length=80)
    desc = models.TextField(verbose_name='Description')
    priority_choices = (
        ("danger", "High"),
        ("warning", "Mid"),
        ("success", "low"),
    )
    priority = models.CharField(verbose_name='优先级', max_length=12, choices=priority_choices, default='danger')

    # 新建、处理中、已解决、已忽略、待反馈、已关闭、重新打开
    status_choices = (
        (1, 'Create'),
        (2, 'Processing'),
        (3, 'Finished'),
        (4, 'Ignored'),
        (5, 'Pending Feedback'),
        (6, 'Closed'),
        (7, 'Reopened'),
    )
    status = models.SmallIntegerField(verbose_name='Status', choices=status_choices, default=1)

    assign = models.ForeignKey(verbose_name='Assign', to='UserInfo', related_name='task', null=True, blank=True,on_delete=models.CASCADE)
    attention = models.ManyToManyField(verbose_name='CC', to='UserInfo', related_name='observe', blank=True)

    start_date = models.DateField(verbose_name='Start Time', null=True, blank=True)
    end_date = models.DateField(verbose_name='Deadline', null=True, blank=True)
    mode_choices = (
        (1, 'Public'),
        (2, 'Private'),
    )
    mode = models.SmallIntegerField(verbose_name='Mode', choices=mode_choices, default=1)

    parent = models.ForeignKey(verbose_name='Parent Issue', to='self', related_name='child', null=True, blank=True,
                               on_delete=models.SET_NULL)

    creator = models.ForeignKey(verbose_name='Creator', to='UserInfo', related_name='create_problems',on_delete=models.CASCADE)

    create_datetime = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)
    latest_update_datetime = models.DateTimeField(verbose_name='Last Update Time', auto_now=True)

    def __str__(self):
        return self.subject

class IssuesReply(models.Model):
    reply_type_choices = (
        (1,'Edit'),
        (2,'Reply')
    )
    reply_type = models.SmallIntegerField(verbose_name='Reply Type',choices=reply_type_choices)

    issues = models.ForeignKey(verbose_name='Issue',to='Issues',on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Content')
    creator = models.ForeignKey(verbose_name='Creator',to='UserInfo',related_name='create_reply',on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)

    reply = models.ForeignKey(verbose_name='reply',to='self',null=True,blank=True,on_delete=models.CASCADE)

class ProjectInvite(models.Model):
    project = models.ForeignKey(verbose_name='Project',to='Project',on_delete=models.CASCADE)
    code = models.CharField(verbose_name='Invite Code',max_length=64,unique=True)
    count = models.PositiveIntegerField(verbose_name='Max Invites',null=True,blank=True,help_text='Empty means unlimited')
    used_count = models.PositiveIntegerField(verbose_name='Invited People',default=0)
    period_choices = (
        (30,'30 Minutes'),
        (60,'1 Hour'),
        (300,'5 Hours'),
        (1440,'24 Hours'),
    )
    period = models.IntegerField(verbose_name='Valid Till',choices=period_choices,default=1440)
    create_datetime = models.DateTimeField(verbose_name='Create At',auto_now_add=True)
    creator = models.ForeignKey(verbose_name='Creator',to='UserInfo',related_name='create_invite',on_delete=models.CASCADE)