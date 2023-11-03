import threading
from queue import Queue

# Create a queue to store code submissions from users
code_queue = Queue()


import subprocess

def execute_java_code(code):
    try:
        java_code = f"""
            
                    {code}
                
            
        """
        command = f'docker run -i -v "$(pwd)":/app -w /app openjdk:11 bash -c "cat > DateAdjuster.java"'

        result = subprocess.run(command, input=java_code, shell=True, capture_output=True, text=True)
        print(result)

        command = 'docker run -i -v "$(pwd)":/app -w /app openjdk:11 bash -c "javac DateAdjuster.java && java DateAdjuster"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        output = result.stdout.strip()
        error_output = result.stderr.strip()

        print("Standard Output:")
        print(output)
        print("Standard Error:")
        print(error_output)
        return output

    except Exception as e:
        return str(e)







def worker():
    while True:
        code_submission = code_queue.get()
        output=execute_java_code(code_submission)
        print(output)
        code_queue.task_done()

NUM_WORKERS = 4 
workers = []
for _ in range(NUM_WORKERS):
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
    workers.append(thread)

def add_code_submission(code):
    code_queue.put(code)
