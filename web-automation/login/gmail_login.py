import os
import shutil


def gmail_login(email: str, password: str) -> None:
    """
    Login to Gmail with the given email password using TagUI and saves the
    chrome profile in docker volume. If profile already exists does nothing
    :param email: user email
    :param password: user password
    :return: None
    """

    new_chrome_profile_path = '/web-automation/puppeteer-scripts/new_user_profile'
    chrome_profile_dir_path = '/web-automation/slack-poc-vol/chrome-profiles'
    puppeteer_script_path = '/web-automation/puppeteer-scripts'

    if os.path.isdir(os.path.join(chrome_profile_dir_path, email)):
        print("profile exists")
        return

    print("chrome profile does not exist")

    print("running puppeteer script..")
    if (
            exit_code := os.system(
                f"xvfb-run --auto-servernum node {os.path.join(puppeteer_script_path, 'gmail_login.js')} {email} {password} {new_chrome_profile_path}")) != 0:
        raise RuntimeError(f"Puppeteer failed with exit_code : {exit_code}")
    print("tagUI flow complete!")

    # save tagUI profile to docker volume
    print("saving chrome profile...")
    shutil.copytree(new_chrome_profile_path, os.path.join(chrome_profile_dir_path, email))
    print("chrome profile saved!")
