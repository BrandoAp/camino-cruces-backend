
import os, requests
from decouple import config


def report_github_issue(title: str, body: str):
    github_token = config("GITHUB_TOKEN")
    repo = "BrandoAp/camino-cruces-backend"

    if not github_token:
        return

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {
        "title": title,
        "body": body,
        "labels": ["bug", "auto-reported"],
    }

    try:
        requests.post(
            f"https://api.github.com/repos/{repo}/issues",
            headers=headers,
            json=payload,
            timeout=10,
        )
    except Exception as e:
        print(f"Error al crear issue: {e}")
