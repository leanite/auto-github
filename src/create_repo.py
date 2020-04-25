import getpass
import os
import sys
import subprocess

from github3 import login
from github3.exceptions import AuthenticationFailed, UnprocessableEntity


def sign_in_to_github():
    username = input("GitHub username: ")
    password = getpass.getpass("GitHub password for {0}: ".format(username))

    if not (username and password):
        raise Exception("Enter GitHub username and password :|")

    session = login(username, password)
    session.me()

    return session


def try_to_create_repo(session, repo_name):
    try:
        new_repo = session.create_repository(repo_name)
        print("Created repository {0} successfully! :D".format(repo_name))
        return new_repo
    except UnprocessableEntity:
        print("Couldn't create repository {0} :(".format(repo_name))
        sys.exit(1)


def after_repo_created(new_repo):
    os.system("mkdir {0}".format(new_repo.name))
    os.chdir(new_repo.name)
    os.system("git init")
    os.system("git remote add origin {0}".format(new_repo.clone_url))
    os.system("echo '# {0}' > README.md".format(new_repo.name))
    os.system("git add .")
    os.system("git commit -m 'Initial commit'")
    p = subprocess.Popen(['git push origin master'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate(input='leanite\n@gbd8nlcl\n')
    print(stdout)
    print(stderr)

def main():
    try:
        session = sign_in_to_github()
        repo_name = input("GitHub new repository name: ")
        new_repo = try_to_create_repo(session, repo_name)
        after_repo_created(new_repo)

    except KeyboardInterrupt:
        print("\nBye! o/")

    except Exception as ex:
        print(ex.args[0])

    except AuthenticationFailed:
        print("Incorrect username or password :S")


if __name__ == "__main__":
    main()
