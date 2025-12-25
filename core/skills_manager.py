import os
import subprocess
import sys

SKILLS_DIR = "skills"

class SkillsManager:
    def __init__(self):
        if not os.path.exists(SKILLS_DIR):
            os.makedirs(SKILLS_DIR)

    def create_skill(self, name, code):
        """Saves a new python script to the skills directory."""
        file_path = os.path.join(SKILLS_DIR, f"{name}.py")
        try:
            with open(file_path, "w") as f:
                f.write(code)
            return f"Skill '{name}' has been successfully created and installed."
        except Exception as e:
            return f"Failed to create skill: {e}"

    def run_skill(self, name, args=""):
        """Executes a previously created skill."""
        file_path = os.path.join(SKILLS_DIR, f"{name}.py")
        if not os.path.exists(file_path):
            return f"Skill '{name}' not found."
        
        try:
            # Run the script as a separate process
            result = subprocess.run([sys.executable, file_path, args], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Skill error: {result.stderr.strip()}"
        except Exception as e:
            return f"Execution error: {e}"

    def list_skills(self):
        return [f.replace(".py", "") for f in os.listdir(SKILLS_DIR) if f.endswith(".py")]
