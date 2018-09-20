import sys

from github3 import GitHub


def main(username):
    anon = GitHub()
    repos = anon.repositories_by(username)

    for short_repository in repos:
        print("\n* {0}".format(short_repository.name))
        print(short_repository.description if short_repository.description is not None else "(no description)")
        print("url: {0}".format(short_repository.html_url))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid argument :S")
        exit(1)

    username = sys.argv[1]
    main(username)