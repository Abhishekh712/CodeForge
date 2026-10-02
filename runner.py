import subprocess
import tempfile
import time
import os


def execute_python(code, input_data="", timeout=2):

    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False
    )

    temp_file.write(code)
    temp_file.close()

    start_time = time.time()

    try:

        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "--pids-limit", "64",
                "-i",
                "-v",
                f"{temp_file.name}:/tmp/submission.py:ro",
                "python:3.12",
                "python",
                "/tmp/submission.py"
            ],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=timeout
        )

        execution_time = time.time() - start_time

        if result.returncode == 0:

            return {
                "status": "Success",
                "output": result.stdout,
                "execution_time": execution_time
            }

        return {
            "status": "Runtime Error",
            "output": result.stderr,
            "execution_time": execution_time
        }

    except subprocess.TimeoutExpired:

        return {
            "status": "Time Limit Exceeded",
            "output": "",
            "execution_time": timeout
        }

    finally:

        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)

if __name__ == "__main__":

    result = execute_python("""
while True:
    pass
""")

    print(result)

