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
        return file_names
    else:
        print(f"Directory '{folder_name}' not found.")
        return []

def execute_policy_file(destination_path, folder_name, file_name):
    file_path = os.path.join(destination_path, folder_name, file_name)
    if os.path.isfile(file_path):
        print(f"Executing policy file: {file_name}")
        # Run custodian run command to execute the specific policy file
        custodian_run_command = f"custodian run --cache-period 0 --output-dir output0 {file_path}"
        proc = subprocess.Popen(custodian_run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()
        print(f"Policy execution output for {file_name}:\n")
        if stdout:
            print(f"Standard Output:\n{stdout}")
        if stderr:
            print(f"Standard Error:\n{stderr}")
        if proc.returncode == 0:
            print(f"Policy {file_name} executed successfully.")
        else:
            print(f"Error executing policy {file_name}.")
    else:
        print(f"File '{file_name}' not found.")

def run_mailer(mailer_config_path):
    if os.path.isfile(mailer_config_path):
        print("Running c7n-mailer...")
        c7n_mailer_command = f"c7n-mailer --run --config {mailer_config_path}"
        subprocess.run(c7n_mailer_command, shell=True)
    else:
        print(f"Mailer config file '{mailer_config_path}' not found.")

def main():
    if len(sys.argv) < 3:
        print("Usage: python script_name.py repo_url folder_name")
        return

    # Replace this with your GitHub repository URL
    repo_url = sys.argv[1]
    destination_path = "/home/soumya/tmp/repo"  # Replace this with your desired destination path

    # Clone the GitHub repository
    cloned_path = clone_repository(repo_url, destination_path)
    print("Git repository cloned successfully")

    # List files in specified folder
    folder_name = sys.argv[2]
    folder_name_with_path = os.path.join(folder_name)
    file_names = list_files_in_folder(cloned_path, folder_name_with_path)

    # Execute the policy files in the specified folder
    for file_name in file_names:
        execute_policy_file(cloned_path, folder_name, file_name)

    
    # Run c7n-mailer with the specified config file
    if len(sys.argv) == 4:
        mailer_config_path = sys.argv[3]
        run_mailer(mailer_config_path)

if __name__ == "__main__":
    main()
