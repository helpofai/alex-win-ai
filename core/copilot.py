import os

class CodebaseExplorer:
    def __init__(self, root_dir="."):
        self.root_dir = root_dir

    def list_files(self):
        """Returns a tree of the current project."""
        tree = []
        for root, dirs, files in os.walk(self.root_dir):
            # Skip hidden and ignore folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            level = root.replace(self.root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            tree.append(f"{indent}{os.path.basename(root)}/")
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                tree.append(f"{sub_indent}{f}")
        return "\n".join(tree)

    def read_file(self, file_path):
        """Reads content of a specific code file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def write_patch(self, file_path, content):
        """Applies a fix/patch to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Patch applied to {file_path}."
        except Exception as e:
            return f"Patch failed: {e}"

