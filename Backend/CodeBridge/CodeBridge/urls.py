"""
URL configuration for CodeBridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CodeBridge_Backend import views
from CodeBridge_Backend import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('signup/', auth.signup, name="signup"),
    path('login/', auth.login, name="login"),
    path('changepass/', auth.changePassword, name="changepass"),
    path('upload', views.FolderUploadView.as_view(), name='upload'),
    path('upload/<int:folder_id>', views.FolderUploadView.as_view(), name='upload'),
    path('file/<int:file_id>', views.FileContentAPIView.as_view(), name ="file"),
    path('logic/<int:file_id>', views.LogicDetailAPIViewNew.as_view(), name ="logic"),
    path('logic/<int:file_id>/<int:logic_id>', views.LogicDetailAPIViewNew.as_view(), name ="logic"),
    path('java/<int:file_id>/<int:logic_id>', views.JavaCodeAPIViewNew.as_view(), name ="java"),
    path('mermaid/<int:file_id>/<int:logic_id>', views.MermaidAPIViewNew.as_view(), name ="mermaid"),
    path('compilejava',views.JavaCompilerView.as_view(), name='compilejava'),
    path('auth/github/callback/', views.github_oauth_callback, name='github_oauth_callback'),
    path('associate-github-token', views.GithubAccessView.as_view(), name='associate_github_token'),
    path('clone-repository/',views.CloneRepositoryAPIView.as_view(),name='clone_repository'),


]
