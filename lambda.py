import os
import subprocess
import time
import sys

def clone_repository(repo_url, destination_path):
    # Append a timestamp to the destination path to make it unique
    timestamp = str(int(time.time()))
    destination_path = os.path.join(destination_path, f"custodian-policy-{timestamp}")

    # Construct the git clone command with the destination path
    clone_command = f"git clone {repo_url} {destination_path}"

    # Run the git clone command using subprocess
    subprocess.run(clone_command, shell=True)

    return destination_path

def list_files_in_folder(destination_path, folder_name):
    folder_path = os.path.join(destination_path, folder_name)
    if os.path.exists(folder_path):
        print(f"File Names inside '{folder_name}' Directory:")
        file_names = [name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))]
        for name in file_names:
            print(name)
    else:
        print(f"Directory '{folder_name}' not found.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python script_name.py repo_url folder_name1 folder_name2 folder_name3 ...")
        return

    # Replace this with your GitHub repository URL
    repo_url = sys.argv[1]
    destination_path = "/home/soumya/tmp/repo"  # Replace this with your desired destination path

    # Clone the GitHub repository
    cloned_path = clone_repository(repo_url, destination_path)
    print("Git repository cloned successfully")

    # List files in specified folders
    for folder_name in sys.argv[2:]:
        folder_name_with_path = os.path.join(folder_name)
        list_files_in_folder(cloned_path, folder_name_with_path)

if __name__ == "__main__":
    main()
