import requests

CURRENT_VERSION = "4.2.0"
# Use /tags endpoint as it detects our 'git tag' pushes immediately
REPO_URL = "https://api.github.com/repos/helpofai/alex-win-ai/tags"

def get_current_version():
    return CURRENT_VERSION

def check_for_updates():
    """Checks the GitHub API for a newer tag."""
    try:
        response = requests.get(REPO_URL, timeout=5)
        if response.status_code == 200:
            tags = response.json()
            if not tags: return None
            
            # The first tag in the list is the most recent
            latest_tag = tags[0].get("name", "").replace("v", "")
            
            if latest_tag and latest_tag > CURRENT_VERSION:
                return latest_tag
    except:
        pass
    return None