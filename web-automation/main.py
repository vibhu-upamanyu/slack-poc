import sys

from login.gmail_login import gmail_login
from login.slack_login import slack_login


def main():
    """Entrypoint function of docker image"""
    if sys.argv[1] == "--gmail-login":
        if len(sys.argv) != 4:
            raise Exception("Incorrect arguments")
        email = sys.argv[2]
        password = sys.argv[3]
        gmail_login(email, password)

    elif sys.argv[1] == "--slack-login":
        if len(sys.argv) != 4:
            raise Exception("Incorrect arguments")
        email = sys.argv[2]
        workspace_name = sys.argv[3]
        slack_login(email, workspace_name)
    else:
        print("Unknown cmd")


if __name__ == '__main__':
    # time.sleep(10000000)
    main()
