import os
import shutil

def clear_temporary_files(directory: str = "tmp"):
    """
    Cleans up any uploaded files in the temporary directory.
    """
    if os.path.exists(directory):
        try:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            print(f"Cleared temporary folder: {directory}")
        except Exception as e:
            print(f"Error clearing temporary files: {e}")

def verify_workspace_structure(base_dir: str):
    """
    Validates that the project directory structure has all necessary components.
    """
    required_dirs = ["database", "mcp_servers", "agents", "skills", "security", "utils", "tests", "docs"]
    missing = []
    for d in required_dirs:
        path = os.path.join(base_dir, d)
        if not os.path.exists(path):
            missing.append(d)
    return missing
