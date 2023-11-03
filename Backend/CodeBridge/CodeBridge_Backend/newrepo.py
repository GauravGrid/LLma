import requests
import git
import os
import tempfile
import json

def create_repository(access_token, repository_name, description):
    url = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }
    data = {
        'name': repository_name,
        'description': description,
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Failed to create GitHub repository: {response.text}")
        return None
    
def get_commit(access_token, owner, repo, default_branch):
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commit_data = response.json()
        return commit_data['sha']
    else:
        print(f"Failed to get latest commit SHA: {response.text}")
        return None


# def push_code(local_path, remote_url, branch_name, access_token):
#     try:
#         repo = git.Repo(local_path)
#         origin = repo.create_remote('origin', remote_url)
#         origin.push(refspec=f'{branch_name}:{branch_name}', auth=(access_token, 'x-oauth-basic'))
#         return True
#     except git.exc.GitCommandError as e:
#         print(f"Error pushing code to GitHub repository: {str(e)}")
#         return False


def create_github_branch(access_token, owner, repo, branch_name, start_sha):
    url = f'https://api.github.com/repos/{owner}/{repo}/git/refs'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }
    data = {
        'ref': f'refs/heads/{branch_name}',
        'sha': start_sha,
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Failed to create GitHub branch: {response.text}")
        return None
    

from urllib.parse import urlparse

def get_git_repo_owner(git_url):
    try:
        parsed_url = urlparse(git_url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        owner = path_parts[0]
        return owner

        return None
    except Exception as e:
        print(f"Error extracting Git repository owner: {str(e)}")
        return None




import os
import tempfile
from git import Repo

from .models import JavaCode, FolderUpload, FileUpload,GitHubRepository

def push_to_github(access_token, repository_url, java_code_entries, branch_name='main', commit_message='Add code'):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_url_with_auth = repository_url.replace("https://", f"https://{access_token}@")

            
            repo = Repo.clone_from(repo_url_with_auth, temp_dir, branch=branch_name)
        

            for java_code_entry in java_code_entries:
                file_upload = java_code_entry.file
                folder_structure = get_folder_structure(file_upload)

                current_dir = temp_dir
                for folder_name in folder_structure:
                    current_dir = os.path.join(current_dir, folder_name)
                    os.makedirs(current_dir, exist_ok=True)
                filename, extension = os.path.splitext(file_upload.filename)
                new_filename = f"{filename}.java"
                file_path = os.path.join(current_dir, new_filename)
                with open(file_path, 'w') as file:
                    file.write(java_code_entry.code)

            repo.git.add("--all")
            repo.index.commit(commit_message)

            origin = repo.remotes.origin
            push_results = origin.push(refspec=f'{branch_name}:{branch_name}', verbose=True)
            for push_info in push_results:
                try:
                    rep = GitHubRepository.objects.get(branch=branch_name,repository_url=repository_url)
                    repo_name = rep.repository_name
                    owner=get_git_repo_owner(repository_url)
                    new_commit_sha = get_commit(access_token=access_token,owner=owner, repo=repo_name,default_branch=branch_name)
                    print(new_commit_sha)
                    update_commit(url=repository_url,branch=branch_name,commit=new_commit_sha)
                except Exception as e:
                    print(e)
        return True
    except Exception as e:
        print(f"Error cloning, making changes, and pushing to GitHub: {str(e)}")
        return False





def get_folder_structure(file_upload):
    folders = []
    current_folder = file_upload.parentFolder
    while current_folder:
        folders.insert(0, current_folder.foldername)  
        current_folder = current_folder.parentFolder
    return folders

def update_commit(url,branch,commit):
    repo = GitHubRepository.objects.get(branch=branch,repository_url=url)
    if repo:
        repo.commit_sha=commit
        repo.save()