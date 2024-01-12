from github import Github

# Your GitHub personal access token
token = "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"

# Your GitHub username
username = "Jownic"

# Your repository name
repo_name = "HomeAssignment"

# Path to the file you want to upload
file_path = "192.168.1.5.txt"

def upload_file_to_github(token, username, repo_name, file_path):
    # Authenticate using your personal access token
    g = Github(token)

    # Get the user
    user = g.get_user(username)

    # Get the repository
    repo = user.get_repo(repo_name)

    # Specify the branch you want to upload to (e.g., 'main' or 'master')
    branch_name = "main"

    try:
        # Get the branch reference
        branch = repo.get_branch(branch_name)
    except Exception as e:
        print(f"Error: {e}")
        print(f"Branch '{branch_name}' not found. Please check the branch name.")
        return

    # Read the content of the file
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Create a new file on GitHub
    try:
        contents = repo.get_contents(file_path, ref=branch_name)
        # If the file already exists, update its content
        repo.update_file(contents.path, "Update file", file_content, contents.sha, branch=branch_name)
        print(f"File '{file_path}' updated successfully.")
    except Exception as e:
        # If the file doesn't exist, create a new file
        repo.create_file(file_path, "Create file", file_content, branch=branch_name)
        print(f"File '{file_path}' created successfully.")

# Call the function to upload the file
upload_file_to_github(token, username, repo_name, file_path)
