import subprocess
import tempfile
import time


def execute_python(code, timeout=3):
    start_time = time.time()

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as file:
            file.write(code)
            file_path = file.name

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        execution_time = time.time() - start_time

        if result.returncode != 0:
            return {
                "status": "Runtime Error",
                "output": result.stderr,
                "execution_time": execution_time
            }

        return {
            "status": "Success",
            "output": result.stdout,
            "execution_time": execution_time
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "Time Limit Exceeded",
            "output": "",
            "execution_time": timeout
        }

if __name__ == "__main__":
    result = execute_python("""
while True:
    pass
""")
    print(result)