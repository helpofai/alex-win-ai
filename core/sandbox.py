import subprocess
import sys
import os
import tempfile

class CodeSandbox:
    def __init__(self):
        pass

    def run_python(self, code):
        """Runs arbitrary python code and returns output."""
        print("[Sandbox] Executing generated code...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(code.encode('utf-8'))
            tmp_path = tmp.name
        
        try:
            result = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            os.remove(tmp_path)
            if result.returncode == 0:
                return f"Output: {result.stdout.strip()}"
            else:
                return f"Error: {result.stderr.strip()}"
        except Exception as e:
            if os.path.exists(tmp_path): os.remove(tmp_path)
            return f"Sandbox Exception: {e}"
