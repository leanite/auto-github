import getpass
import os
import sys

from github3 import login
from github3.exceptions import AuthenticationFailed, UnprocessableEntity


def sign_in_to_github():
    username = input("GitHub username: ")
    password = getpass.getpass("GitHub password for {0}: ".format(username))

    if not (username and password):
        raise Exception("Enter GitHub username and password :|")

    session = login(username, password)
    session.me()

    return session, username, password


def try_to_create_repo(session, repo_name):
    try:
        new_repo = session.create_repository(repo_name)
        print("Created repository {0} successfully! :D".format(repo_name))
        return new_repo
    except UnprocessableEntity:
        print("Couldn't create repository {0} :(".format(repo_name))
        sys.exit(1)


def after_repo_created(new_repo, username, password):
    url_password = password.replace("@","%40")
    url_password = url_password.replace("#","%23")
    os.system("mkdir {0}".format(new_repo.name))
    os.chdir(new_repo.name)
    os.system("git init")
    os.system("git remote add origin {0}".format(new_repo.clone_url))
    os.system("echo '# {0}' > README.md".format(new_repo.name))
    os.system("git add .")
    os.system("git commit -m 'Initial commit'")
    os.system("git push -u https://{0}:{1}@github.com/{0}/{2}.git master".format(username, url_password, new_repo.name))
    

def main():
    try:
        session, username, password = sign_in_to_github()
        repo_name = input("GitHub new repository name: ")
        new_repo = try_to_create_repo(session, repo_name)
        after_repo_created(new_repo, username, password)

    except KeyboardInterrupt:
        print("\nBye! o/")

    except Exception as ex:
        print(ex.args[0])

    except AuthenticationFailed:
        print("Incorrect username or password :S")


if __name__ == "__main__":
    main()
