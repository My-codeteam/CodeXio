import requests
from django.conf import settings


ORG_NAME = "codexmingleteam-sudo"


def get_student_contributions(username):

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    repos_url = f"https://api.github.com/orgs/{ORG_NAME}/repos"

    response = requests.get(repos_url, headers=headers)

    if response.status_code != 200:
        print("GitHub Repo Error:", response.status_code, response.text)
        return []

    repositories = response.json()

    contributed_repos = []

    for repo in repositories:

        contributors_url = repo.get("contributors_url")

        if not contributors_url:
            continue

        try:
            contributor_response = requests.get(
                contributors_url,
                headers=headers,
                timeout=10
            )
        except Exception as e:
            print("Request failed:", e)
            continue

        if contributor_response.status_code != 200:
            continue

        try:
            contributors = contributor_response.json()
        except Exception:
            continue

        for contributor in contributors:

            if contributor.get("login", "").lower() == username.lower():

                contributed_repos.append({
                    "name": repo.get("name"),
                    "description": repo.get("description"),
                    "language": repo.get("language"),
                    "stars": repo.get("stargazers_count", 0),
                    "updated_at": repo.get("updated_at"),
                    "repo_url": repo.get("html_url"),
                    "contributions": contributor.get("contributions", 0)
                })

                break

    print("Found repos:", len(contributed_repos))

    return sorted(
        contributed_repos,
        key=lambda x: x["updated_at"] or "",
        reverse=True
    )