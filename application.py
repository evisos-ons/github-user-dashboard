import os

import requests
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from jinja2 import ChainableUndefined

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mysecret")  # Use a secure secret key in production
app.jinja_env.undefined = ChainableUndefined


@app.route("/", methods=["GET"])
def hello_world():
    github_token = os.getenv("GITHUB_TOKEN")
    user_info = {}
    followers = []
    repos = []
    error_message = request.args.get("error")

    if github_token:
        headers = {"Authorization": f"token {github_token}"}

        # Fetch user info
        user_response = requests.get("https://api.github.com/user", headers=headers)
        if user_response.status_code == 200:
            user_info = user_response.json()
        else:
            user_info = {"error": f"Failed to fetch user info, status code: {user_response.status_code}"}

        # Fetch followers
        followers_response = requests.get("https://api.github.com/user/followers", headers=headers)
        if followers_response.status_code == 200:
            followers_data = followers_response.json()
            followers = [follower["login"] for follower in followers_data]
        else:
            followers = {"error": f"Failed to fetch followers, status code: {followers_response.status_code}"}
    
        # Fetch followers
        repos_response = requests.get("https://api.github.com/users/evisos-ons/repos", headers=headers)
        if repos_response.status_code == 200:
            repos_data = repos_response.json()
            for repo in repos_data:
                repo_info = {
                    "id": repo["id"],
                    "full_name": repo["full_name"],
                    "private": repo["private"],
                    "description": repo["description"],
                    "fork": repo["fork"]
                }
                repos.append(repo_info)
        else:
            repos = {"error": f"Failed to fetch repositories, status code: {repos_response.status_code}"} 
            user_info = {"error": "GitHub token not found in environment variables."}

    return render_template(
        "index.html",
        param="Hello world",
        user_info=user_info,
        followers=followers,
        repos=repos,
        error_message=error_message,
    )


@app.route("/saveField", methods=["POST"])
def save_field():
    # Retrieve the field and new value from the form data
    field = request.form.get("field")
    new_value = request.form.get("value")
    github_token = os.getenv("GITHUB_TOKEN")
    print(field, new_value, request.form)

    if not github_token:
        print("GitHub token not found in environment variables.")
        return redirect(url_for("hello_world", error="GitHub token not found"))

    headers = {
        "Authorization": f"token {github_token}",
        "Content-Type": "application/json",
    }
    data = {}

    # Map field names to GitHub API fields
    if field == "twitter_username":
        data["twitter_username"] = new_value if new_value else None
    elif field == "hireable":
        data["hireable"] = True if new_value == "true" else (False if new_value == "false" else None)
    elif new_value == None:
        return redirect(url_for("hello_world", error="Value cannot be empty"))
    else:
        data[field] = new_value

    # Update user info on GitHub
    response = requests.patch("https://api.github.com/user", headers=headers, json=data)
    if response.status_code == 200:
        return redirect(url_for("hello_world"))
    else:
        # Handle error
        print(f"Failed to update {field}, status code: {response.status_code}")
        return redirect(url_for("hello_world", error=f"Failed to update {field}"))


if __name__ == "__main__":
    app.run()
