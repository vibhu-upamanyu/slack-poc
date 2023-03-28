import os
import shutil


def slack_login(email: str, workspace_name : str) -> None:
    """
    Login to slack using Google auth from the google account logged in chrome profile
    :param workspace_name: Name of the slack workspace
    :param email: admin email to log in to slack
    :return:
    """

    puppeteer_script_path = '/web-automation/puppeteer-scripts'
    chrome_profile_dir_path = '/web-automation/slack-poc-vol/chrome-profiles'


    if (exit_code := os.system(f"xvfb-run --auto-servernum node {os.path.join(puppeteer_script_path, 'slack_login.js')} {workspace_name} {os.path.join(chrome_profile_dir_path, email)}")) != 0:
        raise RuntimeError(f"Puppeteer failed with exit_code : {exit_code}")


