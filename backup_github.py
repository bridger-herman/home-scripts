'''
backup_github.py

Bridger Herman <firstname.g.lastname@gmail.com>

Clones a bunch of GitHub repositories to a specified path.
'''
import os
from getpass import getpass
import json
import time
from github import Github
from github import Auth
import github.Repository
import pygit2
from subprocess import Popen

SECRETS_FILE = 'secrets.json'
_SECRETS_SCHEMA = {
    'github_token': 'str',
    'github_username': 'str',
    'github_parent_clone_path': 'str <path>',
    'github_ssh_keypair': 'str <path>'
}
BASE_URL = 'https://github.umn.edu/api/v3'


def main():
    with open(SECRETS_FILE) as fin:
        contents = json.load(fin)
        auth = Auth.Token(contents['github_token'])
        gh_username = contents['github_username']
        clone_path = contents['github_parent_clone_path']
        # https://www.pygit2.org/recipes/git-clone-ssh.html
        clone_ssh_keypair = contents['github_ssh_keypair']
        keypair = pygit2.Keypair('git', clone_ssh_keypair + '.pub', clone_ssh_keypair, getpass("Passphrase for " + clone_ssh_keypair + ": "))
        git_auth = pygit2.RemoteCallbacks(credentials=keypair)

    g = Github(auth=auth, base_url=BASE_URL)

    to_clone: set[github.Repository.Repository] = set()

    start_time = time.time()
    for repo in g.get_user().get_repos():
        if repo.owner.login == gh_username:
            to_clone.add(repo)
    end_time = time.time()
    print('searched through repos:', end_time - start_time, 'sec')

    start_time = time.time()
    for repo in to_clone:
        try:
            print('cloning', repo, repo.ssh_url)
            repo_clone = pygit2.clone_repository(
                repo.ssh_url,
                os.path.join(clone_path, repo.name),
                callbacks=git_auth)
            print(repo_clone)
        except ValueError:
            print(repo.name, 'already exists')
    end_time = time.time()
    print('cloned repos:', end_time - start_time, 'sec')

    g.close()

if __name__ == '__main__':
    main()