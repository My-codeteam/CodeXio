import requests
from django.conf import settings


ORG_NAME = "codexmingleteam-sudo"

GITHUB_HEADERS = {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_student_contributions(username):
    """
    Get a student's GitHub activity within the CodexMingle GitHub organization.

    Returns:
        {
            "projects": int,
            "commits": int,
            "stars": int,
            "username": str,
            "connected": bool,
            "error": bool,
        }
    """

    # Student has not connected a GitHub account
    if not username:
        return {
            "projects": 0,
            "commits": 0,
            "stars": 0,
            "username": None,
            "connected": False,
            "error": False,
        }

    projects = 0
    total_commits = 0
    total_stars = 0

    page = 1

    while True:

        repos_url = (
            f"https://api.github.com/orgs/{ORG_NAME}/repos"
            f"?per_page=100&page={page}"
        )

        try:
            response = requests.get(
                repos_url,
                headers=GITHUB_HEADERS,
                timeout=10
            )
        except requests.RequestException as e:
            print("GitHub Repository Request Error:", e)

            return {
                "projects": 0,
                "commits": 0,
                "stars": 0,
                "username": username,
                "connected": True,
                "error": True,
            }

        if response.status_code != 200:
            print(
                "GitHub Repo Error:",
                response.status_code,
                response.text
            )

            return {
                "projects": 0,
                "commits": 0,
                "stars": 0,
                "username": username,
                "connected": True,
                "error": True,
            }

        repositories = response.json()

        if not repositories:
            break

        for repo in repositories:

            contributors_url = repo.get("contributors_url")

            if not contributors_url:
                continue

            contributor_page = 1

            while True:

                url = (
                    f"{contributors_url}"
                    f"?per_page=100&page={contributor_page}"
                )

                try:
                    contributor_response = requests.get(
                        url,
                        headers=GITHUB_HEADERS,
                        timeout=10
                    )
                except requests.RequestException as e:
                    print(
                        "GitHub Contributor Request Error:",
                        e
                    )
                    break

                if contributor_response.status_code != 200:
                    print(
                        "GitHub Contributor Error:",
                        contributor_response.status_code
                    )
                    break

                try:
                    contributors = contributor_response.json()
                except ValueError:
                    break

                if not contributors:
                    break

                found_student = False

                for contributor in contributors:

                    contributor_username = contributor.get("login", "")

                    if contributor_username.lower() == username.lower():

                        projects += 1

                        total_commits += contributor.get(
                            "contributions",
                            0
                        )

                        total_stars += repo.get(
                            "stargazers_count",
                            0
                        )

                        found_student = True
                        break

                # We found the student in this repository.
                if found_student:
                    break

                # If fewer than 100 contributors were returned,
                # there is no next page.
                if len(contributors) < 100:
                    break

                contributor_page += 1

        # If fewer than 100 repositories were returned,
        # there is no next page.
        if len(repositories) < 100:
            break

        page += 1

    return {
        "projects": projects,
        "commits": total_commits,
        "stars": total_stars,
        "username": username,
        "connected": True,
        "error": False,
    }