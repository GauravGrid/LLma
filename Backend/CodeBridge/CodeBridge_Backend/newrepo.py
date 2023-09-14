import requests
import git


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


def push_code(local_path, remote_url, branch_name, access_token):
    try:
        repo = git.Repo(local_path)
        origin = repo.create_remote('origin', remote_url)
        origin.push(refspec=f'{branch_name}:{branch_name}', auth=(access_token, 'x-oauth-basic'))
        return True
    except git.exc.GitCommandError as e:
        print(f"Error pushing code to GitHub repository: {str(e)}")
        return False


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

url = 'https://github.com/vinayjain05/BrokerApp'
get_git_repo_owner(url)