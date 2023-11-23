from github import Github
import os
import yaml
from tkinter import Tk, filedialog
from tqdm import tqdm
import threading
import time
import traceback

BANNER = """
\033[94m   __  __      __                __         
  / / / /___  / /___  ____ _____/ /__  _____
 / / / / __ \/ / __ \/ __ `/ __  / _ \/ ___/
/ /_/ / /_/ / / /_/ / /_/ / /_/ /  __/ /    
\____/ .___/_/\____/\__,_/\__,_/\___/_/     
    /_/                                     
\033[0m
"""

def load_config():
    if os.path.exists('config.yml'):
        with open('config.yml', 'r') as config_file:
            config = yaml.safe_load(config_file)
        return config
    else:
        return None

def save_config(config):
    with open('config.yml', 'w') as config_file:
        yaml.dump(config, config_file)

def get_github_config():
    config = load_config()
    if config is None:
        print("You haven't made a config!")
        github_token = input("Please enter your GitHub Token: ")
        repository_name = input("Please enter your repo: ")
        config = {
            'github_token': github_token,
            'repository_name': repository_name
        }
        save_config(config)
    return config['github_token'], config['repository_name']

def upload_to_github(token, repo_name, file_path, progress_bar):
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(repo_name)

    file_name = os.path.basename(file_path)
    file_content = open(file_path, 'rb').read()
    
    existing_file = None
    sha = None
    try:
        existing_file = repo.get_contents(f"videos/{file_name}")
        sha = existing_file.sha
    except Exception as e:
        pass

    try:
        with tqdm(total=len(file_content), unit='B', unit_scale=True, unit_divisor=1024, disable=False) as pbar:
            def update_progress():
                while not pbar.n >= pbar.total:
                    pbar.update(pbar.total - pbar.n)
                pbar.close()

            progress_thread = threading.Thread(target=update_progress)
            progress_thread.start()

            if sha:
                repo.update_file(existing_file.path, f"Update {file_name}", file_content, sha=sha)
            else:
                repo.create_file(f"videos/{file_name}", f"Upload {file_name}", file_content)
            progress_thread.join()

        video_url = f"https://cryzis.uk/videos/{file_name.replace(' ', '%20')}"
        print(f"\033[92mVideo uploaded at: {video_url}\033[0m")
    except Exception as e:
        traceback.print_exc()
        print(f"\033[91mError uploading video: {str(e)}\033[0m")

def get_file_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

if __name__ == "__main__":
    print(BANNER)
    
    while True:
        github_token, repository_name = get_github_config()
        print("\033[93mPlease select the video file using the dialog.\033[0m")
        video_file_path = get_file_path()

        if video_file_path:
            try:
                upload_to_github(github_token, repository_name, video_file_path, tqdm)
            except Exception as e:
                traceback.print_exc()
                print(f"\033[91mError during upload: {str(e)}\033[0m")
        else:
            print("\033[91mNo file selected.\033[0m")

        restart_input = input("\033[96mPress Enter to restart or type 'exit' to close: \033[0m").strip()
        if restart_input.lower() == 'exit':
            break
