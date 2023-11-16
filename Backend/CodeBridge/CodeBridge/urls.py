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
    path('codegen/<int:file_id>', views.CodeGenAPIViewNew.as_view(), name ="java"),
    path('codegen/<int:file_id>/<int:logic_id>', views.CodeGenAPIViewNew.as_view(), name ="java"),
    path('mermaid/<int:file_id>', views.MermaidAPIViewNew.as_view(), name ="mermaid"),
    path('mermaid/<int:file_id>/<int:logic_id>', views.MermaidAPIViewNew.as_view(), name ="mermaid"),
    path('compilejava',views.JavaCompilerView.as_view(), name='compilejava'),
    path('auth/github/callback/', views.github_oauth_callback, name='github_oauth_callback'),
    path('associate-github-token', views.GithubAccessView.as_view(), name='associate_github_token'),
    path('clone-repository/',views.CloneRepositoryAPIView.as_view(),name='clone_repository'),
    path('create-git-repo/',views.CreateGitHubRepository.as_view(),name='create_git_repo'),
    path('push-to-git/',views.PushCodeToGitHub.as_view(),name='push_to_git'),
    path('create-branch/',views.CreateGitHubBranch.as_view(),name='create_branch'),
    path('get-branch/',views.ListBranches.as_view(),name='list_branch'),
    path('git-pull/',views.PullCodeFromGitHub.as_view(),name='git_pull'),
    path('gen-share-code/',views.GenerateUUID.as_view(),name='generate_share_code'),
    path('get-access/',views.AccessRepository.as_view(),name='get_access_to_repository'),
    
    # Urls for Higher Level business Logic For a repo
    path('api/business_logic/', views.HigherLevelBusinessLogic.as_view(), name='higher_level_business_logic'),
    
    # Urls for Higher Level Mermaid Diagram For a repo
    path('api/mermaid_diagram/', views.HigherLevelMermaidDiagram.as_view(), name='higher_level_mermaid_diagram'),
    
    # Urls for Higher Level Mermaid Flowchart For a repo
    path('api/mermaid_flowchart/', views.HigherLevelMermaidFlowchart.as_view(), name='higher_level_mermaid_flowchart'),
    
    # Urls for Higher Level business Logic for files in context of HS023.txt
    path('api/business_logic_023/', views.HigherLevelBL023.as_view(), name='business_logic_023'),
    
    # Urls for Higher Level business Logic for files in context of HS06.txt
    path('api/business_logic_06/', views.HigherLevelBL06.as_view(), name='business_logic_06'),
    
    # Urls for Higher Level business Logic for files in context of HS06N.txt
    path('api/business_logic_06N/', views.HigherLevelBL06N.as_view(), name='business_logic_06N'),
    
    # Urls for Higher Level business Logic for files in context of customer search files
    path('api/business_logic_customer_search/', views.HigherLevelBLcustomersearch.as_view(), name='business_logic_customer_search'),
    
    # Urls for Higher Level Mermaid Diagram for files in context of customer search files
    path('api/mermaid_diagram_customer_search/', views.HigherLevelMDcustomersearch.as_view(), name='mermaid_diagram_customer_search'),
    
    # Urls for Higher Level Mermaid Flowchart for files in context of customer search files
    path('api/mermaid_flowchart_customer_search/', views.HigherLevelMFcustomersearch.as_view(), name='mermaid_flowchart_customer_search'),
    
    # Urls for Pratice
    path('api/business/', views.HigherLevelBusinessLogicP.as_view(), name='higher_level_business_logic'),
]
