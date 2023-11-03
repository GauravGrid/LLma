from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid


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
    rootFolder = models.IntegerField(null=True)


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

class GitHubRepository(models.Model):
    owner = models.CharField(max_length=256)
    repository_name = models.CharField(max_length=256)
    repository_url = models.URLField()
    branch = models.CharField(max_length=256)
    commit_sha = models.CharField(max_length=64, blank=True, null=True)
    collaborators = models.ManyToManyField(User, related_name='collaborating_repositories')
    source_code = models.ForeignKey(FolderUpload, on_delete=models.CASCADE, null=True)

class JavaCode(models.Model):
    code = models.TextField()
    logic = models.ForeignKey(Logic,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    file = models.ForeignKey(FileUpload,null=True,on_delete=models.CASCADE)
    repository = models.ForeignKey(GitHubRepository,null=True,on_delete=models.CASCADE)
    language_converted = models.CharField(max_length=256,null=True)

class ClonedRepository(models.Model):
    users = models.ManyToManyField(User)
    repository_name = models.CharField(max_length=256)
    repository_url = models.URLField()
    branch = models.CharField(max_length=100)
    folder_id = models.ForeignKey(FolderUpload, null=True, on_delete=models.CASCADE) 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.repository_name} (Cloned by {', '.join(user.username for user in self.users.all())})"
    

# class GitHubCollaborator(models.Model):
#     repository = models.ForeignKey(GitHubRepository, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

class ShareCode(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    folder_structure = models.ForeignKey(FolderUpload, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='shared_links')
