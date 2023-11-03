import subprocess

def compile_and_execute_java(java_code):
    # Compile the Java code using javac
    compile_command = ["javac"]
    try:
        subprocess.run(compile_command, input=java_code, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Compilation failed:", e)
        return

    class_name = java_code.split("class ")[1].split()[0].strip()

    execute_command = ["java", class_name]
    try:
        subprocess.run(execute_command, check=True)
    except subprocess.CalledProcessError as e:
        print("Execution failed:", e)



