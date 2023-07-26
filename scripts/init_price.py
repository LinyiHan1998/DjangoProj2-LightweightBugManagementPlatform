import base
from web import models

# class PriceStrategy(models.Model):
#     category_choices=(
#         (1,'Free'),
#         (2,'VIP'),
#         (3,'SVIP'),
#         (4,'other')
#     )
#     category = models.SmallIntegerField(verbose_name='Charge Category',default=1,choices=category_choices)
#     title = models.CharField(verbose_name='Title',max_length=32)
#     price = models.PositiveIntegerField(verbose_name='Price')
#
#     project_num = models.PositiveIntegerField(verbose_name='Max Project Number')
#     project_mem = models.PositiveIntegerField(verbose_name='Max Project Member')
#     project_space = models.PositiveIntegerField(verbose_name='Project Space')
#     per_file_size = models.PositiveIntegerField(verbose_name='Per file size (M)')
#
#     create_datetime = models.DateTimeField(verbose_name='Create Time',auto_now_add=True)
def run():
    exists = models.PriceStrategy.objects.filter(category=1,title='Free').exists()
    if not exists:
        models.PriceStrategy.objects.create(category=1,title='Free', price=0, project_num=3, project_mem=2, project_space=20, per_file_size=5)
# models.PriceStrategy.objects.create(category=2,title='VIP', price=199, project_num=3, project_mem=2, project_space=20, per_file_size=5)
# models.PriceStrategy.objects.create(category=3,title='SVIP', price=299, project_num=3, project_mem=2, project_space=20, per_file_size=5)

if __name__ =='__main__':
    run()