import requests
def enable_github_pages(username, repo_name, token):
    url = f"https://api.github.com/repos/{username}/{repo_name}/pages"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
        }
    data = {
        "source": {
            "branch": "gh-pages",
            "path": "/"
            }
        }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("GitHub Pages have been successfully enabled.")
    else:
        print(f"Failed to enable GitHub Pages: {response.status_code}")
        print(response.json())
def main():
    token = input("Enter your GitHub token: ")
    owner = input("Enter your user name: ")
    repo_name = input("Enter the repository name: ")
    enable_github_pages(owner, repo_name, token)

if __name__ == '__main__':
    main()