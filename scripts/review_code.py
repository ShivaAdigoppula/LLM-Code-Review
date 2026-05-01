import json
import os
from openai import OpenAI
import requests

DIFF_FILE = "diff.txt"
OUTPUT_FILE = "review_output.md"

def read_diff():
    if not os.path.exists(DIFF_FILE):
        return ""
    with open(DIFF_FILE, "r", encoding="utf-8") as f:
        return f.read()

def truncate_diff(diff_text, max_chars=12000):
    if len(diff_text) <= max_chars:
        return diff_text
    return diff_text[:max_chars] + "\n\n[Diff truncated because it is too large]"

def get_pr_number():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path:
        return None
    with open(event_path, "r", encoding="utf-8") as f:
        event = json.load(f)
    return event.get("pull_request", {}).get("number")

def call_llm(diff_text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
You are a senior software reviewer.

Review the following git diff and return:
1. A short summary of what changed
2. Possible bugs or risks
3. Code quality suggestions
4. Security concerns if any

Git diff:
{diff_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert software code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def save_output(review_text):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(review_text)

def post_comment_to_github(review_text):
    pr_number = get_pr_number()
    repo = os.getenv("GITHUB_REPOSITORY")
    token = os.getenv("GITHUB_TOKEN")

    if not pr_number or not repo or not token:
        print("Missing PR number, repo, or token.")
        return

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "body": f"## LLM Code Review\n\n{review_text}"
    }

    response = requests.post(url, headers=headers, json=data)
    print("GitHub comment status:", response.status_code)
    print(response.text)

def main():
    diff_text = read_diff()

    if not diff_text.strip():
        review_text = "No code changes found in the pull request diff."
    else:
        diff_text = truncate_diff(diff_text)
        review_text = call_llm(diff_text)

    save_output(review_text)
    post_comment_to_github(review_text)

if __name__ == "__main__":
    main()