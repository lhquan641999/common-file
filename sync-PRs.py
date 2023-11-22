import requests
import os

# Constants
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}
ORIGINAL_REPO = 'organization/micro-servicea/backend'
FORKED_REPO = 'your-username/micro-servicea-new/backend'

def list_pull_requests(repo):
    url = f'https://api.github.com/repos/{repo}/pulls'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return [{
            'title': pr['title'],
            'body': pr['body'],
            'head': pr['head']['ref'],
            'base': pr['base']['ref'],
            'user': pr['user']['login']
        } for pr in response.json()]
    else:
        raise Exception(f'Error fetching pull requests: {response.content}')

def create_pull_request(title, body, head, base, user, repo):
    head_ref = f"{user}:{head}"
    url = f'https://api.github.com/repos/{repo}/pulls'
    payload = {
        'title': title,
        'body': body,
        'head': head_ref,
        'base': base
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 201:
        print(f'Pull request created: {response.json()["html_url"]}')
    else:
        raise Exception(f'Error creating pull request: {response.content}')

def main():
    prs = list_pull_requests(ORIGINAL_REPO)
    for pr in prs:
        # Additional logic for branch replication
        create_pull_request(
            title=pr['title'],
            body=pr['body'],
            head=pr['head'],
            base=pr['base'],
            user=pr['user'],
            repo=FORKED_REPO
        )

if __name__ == '__main__':
    main()
