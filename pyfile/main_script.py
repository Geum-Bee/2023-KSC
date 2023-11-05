import subprocess

parameter_values = [8000]

# 코드 파일들의 리스트
code_files = ["sampling.py", "get_segments.py", "get_connected_path.py", "is_balanced_path.py"]

for value in parameter_values:
    for file in code_files:
        subprocess.run(["python", file, str(value)])
