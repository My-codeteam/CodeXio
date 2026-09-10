import requests
from django.conf import settings


# GitHub account that owns CodexMingle projects
GITHUB_OWNER = "codexmingleteam-sudo"


def get_student_contributions(username):
    """
    Get a student's contribution summary across
    CodexMingle GitHub repositories.

    Returns:
        {
            "username": "...",
            "projects_contributed": 0,
            "total_commits": 0,
            "total_stars": 0,
            "connected": True/False,
            "error": True/False,
            "error_message": "..."
        }
    """

    # No GitHub username connected

    if not username:
        return {
            "username": "",
            "projects_contributed": 0,
            "total_commits": 0,
            "total_stars": 0,
            "connected": False,
            "error": False,
            "error_message": "",
        }

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    # Get repositories owned by CodexMingle

    repositories = []
    page = 1

    while True:

        repos_url = (
            f"https://api.github.com/users/"
            f"{GITHUB_OWNER}/repos"
        )

        try:
            response = requests.get(
                repos_url,
                headers=headers,
                params={
                    "per_page": 100,
                    "page": page,
                    "type": "all",
                },
                timeout=10,
            )

        except requests.RequestException as e:

            return {
                "username": username,
                "projects_contributed": 0,
                "total_commits": 0,
                "total_stars": 0,
                "connected": False,
                "error": True,
                "error_message": str(e),
            }

        # GitHub returned an error

        if response.status_code != 200:

            return {
                "username": username,
                "projects_contributed": 0,
                "total_commits": 0,
                "total_stars": 0,
                "connected": False,
                "error": True,
                "error_message": response.text,
            }

        batch = response.json()

        if not batch:
            break

        repositories.extend(batch)

        # No more pages
        if len(batch) < 100:
            break

        page += 1

    # Calculate student's contributions

    projects_contributed = 0
    total_commits = 0
    total_stars = 0

    for repo in repositories:

        repo_name = repo.get("name")

        if not repo_name:
            continue

        contributors_url = (
            f"https://api.github.com/repos/"
            f"{GITHUB_OWNER}/{repo_name}/contributors"
        )

        contributor_page = 1
        student_found = False

        while True:

            try:
                contributor_response = requests.get(
                    contributors_url,
                    headers=headers,
                    params={
                        "per_page": 100,
                        "page": contributor_page,
                    },
                    timeout=10,
                )

            except requests.RequestException as e:

                print(
                    f"GitHub contributor request failed "
                    f"for {repo_name}: {e}"
                )

                break

            if contributor_response.status_code != 200:
                break

            contributors = contributor_response.json()

            if not contributors:
                break

            # Find the student

            for contributor in contributors:

                contributor_username = contributor.get(
                    "login",
                    ""
                )

                if (
                    contributor_username.lower()
                    == username.lower()
                ):

                    contributions = contributor.get(
                        "contributions",
                        0
                    )

                    # Number of contributions/commits
                    total_commits += contributions

                    # Count this project once
                    projects_contributed += 1

                    # Add repository stars once
                    total_stars += repo.get(
                        "stargazers_count",
                        0
                    )

                    student_found = True

                    break

            if student_found:
                break

            # Continue pagination if necessary
            if len(contributors) < 100:
                break

            contributor_page += 1

    # Return GitHub summary

    return {
        "username": username,
        "projects_contributed": projects_contributed,
        "total_commits": total_commits,
        "total_stars": total_stars,
        "connected": True,
        "error": False,
        "error_message": "",
    }