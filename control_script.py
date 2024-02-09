import subprocess
import time

def run_ppe():
   subprocess.run(["python", "ppe.py"])

def run_main():
   subprocess.run(["python", "main.py"])

while True:
   try:
       run_ppe()
   except subprocess.CalledProcessError as e:
       print(f"ppe.py exited with error: {e}")

   try:
       run_main()
   except subprocess.CalledProcessError as e:
       print(f"main.py exited with error: {e}")

   time.sleep(0)  # Add a brief pause between iterations
