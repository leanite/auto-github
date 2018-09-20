import os
import sys

import pycurl as pycurl


def main(language):
    url = "https://raw.githubusercontent.com/leanite/gitignores/master/gitignore-{0} -o .gitignore".format(language)
    filename = ".gitignore"

    with open(filename, "wb") as f:
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, f)
        c.perform()

        if c.getinfo(c.RESPONSE_CODE) == 200:
            print(".gitignore downloaded :)")
            print("Total time: {0}s".format(c.getinfo(c.TOTAL_TIME)))
        else:
            print("Error downloading .gitignore :(")
            os.remove(filename)

        c.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid argument :S")
        exit(1)

    language_arg = sys.argv[1]
    main(language_arg)