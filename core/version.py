import requests

CURRENT_VERSION = "4.1.0"
REPO_URL = "https://api.github.com/repos/helpofai/alex-win-ai/releases/latest"

def get_current_version():
    return CURRENT_VERSION

def check_for_updates():
    """Checks the GitHub API for a newer version tag."""
    try:
        response = requests.get(REPO_URL, timeout=5)
        if response.status_code == 200:
            latest_data = response.json()
            latest_version = latest_data.get("tag_name", "").replace("v", "")
            if latest_version and latest_version > CURRENT_VERSION:
                return latest_version
    except:
        pass
    return None
