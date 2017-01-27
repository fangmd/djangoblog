from django.db import models


# Create your models here.

class FileModel(models.Model):
    """
    文件模型：时间，文件名，大小，描述, 文件地址
    """
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    file_name = models.CharField('文件名', max_length=70)
    file_length = models.IntegerField('文件大小', null=True)
    desc = models.CharField('描述', max_length=120, null=True)
    file_path = models.FilePathField('文件地址')
    file = models.FileField(upload_to='upload_file/%Y/%m/%d', default='asd')

    def __str__(self):
        return self.file_name

    class Meta:
        pass
