import subprocess
import sys

def run_generated_file(file_path: str) -> str:
    result = subprocess.run(
        [sys.executable, file_path],
        check=True,
        capture_output=True,
        text=True
    )
    return result.stdout