from django.db import models

class User(models.Model):
    username = models.CharField(max_length=256,null = False, unique= True,primary_key=True)
    email = models.CharField(max_length=256,null = False)
    password = models.CharField(max_length=256,null = False)

    

class FolderUpload(models.Model):
    folderId = models.AutoField(primary_key=True)
    foldername = models.CharField(max_length=2048, null=False)
    parentFolder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User,null = True, on_delete=models.CASCADE)


class FileUpload(models.Model):
    filename = models.CharField(max_length=2048, null=False)
    fileId = models.AutoField(primary_key=True)
    file = models.TextField()
    parentFolder = models.ForeignKey(FolderUpload, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)

class Logic(models.Model):
    logic = models.TextField()
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    file = models.ForeignKey(FileUpload,null=True,on_delete=models.CASCADE)

class MermaidDiagrams(models.Model):
    classDiagram = models.TextField()
    flowChart = models.TextField()
    logic = models.ForeignKey(Logic,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    file = models.ForeignKey(FileUpload,null=True,on_delete=models.CASCADE)

class JavaCode(models.Model):
    code = models.TextField()
    logic = models.ForeignKey(Logic,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    file = models.ForeignKey(FileUpload,null=True,on_delete=models.CASCADE)
