from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(models.Model):
    username = models.CharField(max_length=256,null = False, unique= True,primary_key=True)
    email = models.CharField(max_length=256,null = False)
    password = models.CharField(max_length=256,null = False)
    access_token = models.CharField(max_length=512, null=True, blank=True)
   

    

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
    code_language = models.CharField(max_length=50, null=True)  


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


class ClonedRepository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository_name = models.CharField(max_length=256)
    repository_url = models.URLField()
    branch = models.CharField(max_length=100)
    parent_folder = models.ForeignKey(FolderUpload,null=True,on_delete=models.CASCADE) 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.repository_name} (Cloned by {self.user.username})"