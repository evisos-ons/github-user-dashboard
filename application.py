from flask import Flask, render_template, request, redirect, url_for, session
from jinja2 import ChainableUndefined
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mysecret")  # Use a secure secret key in production
app.jinja_env.undefined = ChainableUndefined
@app.route("/", methods=["GET"])
def hello_world():
    github_token = os.getenv("GITHUB_TOKEN")
    user_info = {}
    followers = []
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
            followers = [follower['login'] for follower in followers_data]
        else:
            followers = {"error": f"Failed to fetch followers, status code: {followers_response.status_code}"}
    else:
        user_info = {"error": "GitHub token not found in environment variables."}

    return render_template("index.html", param="Hello world", user_info=user_info, followers=followers, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
