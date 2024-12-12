import requests
import shutil
import base64
import os

def create_repo(token, repo_name):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Repository '{repo_name}' created successfully.")
    else:
        print(f"Failed to create repository: {response.json()}")

def upload_file_to_github(username, repository, token, file_path, github_path, branch='main'):
    with open(file_path, 'rb') as file:
        content = base64.b64encode(file.read()).decode('utf-8')
    
    url = f'https://api.github.com/repos/{username}/{repository}/contents/{github_path}'
    
    data = {
        'message': f'Add {github_path}',
        'content': content,
        'branch': branch
    }
    
    response = requests.put(url, json=data, auth=(username, token))
    if response.status_code == 201:
        print(f'Successfully uploaded {github_path}')
    else:
        print(f'Failed to upload {github_path}: {response.status_code}, {response.text}')

def create_github_directory(username, repository, token, github_path, branch='main'):
    url = f'https://api.github.com/repos/{username}/{repository}/contents/{github_path}/.gitkeep'
    
    data = {
        'message': f'Create directory {github_path}',
        'content': base64.b64encode(b'').decode('utf-8'),
        'branch': branch
    }
    
    response = requests.put(url, json=data, auth=(username, token))
    if response.status_code == 201:
        print(f'Successfully created directory {github_path}')
    else:
        print(f'Failed to create directory {github_path}: {response.status_code}, {response.text}')

def upload_folder_to_github(username, repository, token, folder_path, branch='main'):
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            github_path = os.path.relpath(dir_path, folder_path).replace("\\", "/")
            create_github_directory(username, repository, token, github_path, branch)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            github_path = os.path.relpath(file_path, folder_path).replace("\\", "/")
            upload_file_to_github(username, repository, token, file_path, github_path, branch)

def set_workflow_permissions(username, repo_name, token):
    url = f'https://api.github.com/repos/{username}/{repo_name}/actions/permissions/workflow' 
    headers = { 
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
        } 
    data = {
        'default_workflow_permissions': 'write',
        'can_approve_pull_request_reviews': False
        }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 204:
        print("Workflow permissions set to read and write.")
    else:
        print(f"Failed to set workflow permissions: {response.json()}")

def run_workflow(username, repo_name, token, workflow_id):
    url = f'https://api.github.com/repos/{username}/{repo_name}/actions/workflows/{workflow_id}/dispatches'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'ref': 'main'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 204:
        print('Workflow run triggered successfully.')
    else:
        print(f'Failed to trigger workflow run: {response.json()}')

def main():
    global commit_message
    token = input("Enter your GitHub token: ")
    owner = input("Enter your user name: ")
    repo_name = input("Enter the repository name: ")
    create_repo(token, repo_name)
    folder_path = "pygbag_builder_build"
    commit_message = "Initial commit of pygbag_builder_build contents"
    upload_folder_to_github(owner, repo_name, token, folder_path)
    set_workflow_permissions(owner, repo_name, token)
    run_workflow(owner, repo_name, token, "pygbag.yml")
    #enable_github_pages(owner, repo_name, token)

if __name__ == "__main__":
    main()