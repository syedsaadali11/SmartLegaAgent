import os

def list_top_folders(path="."):
    print("📁 Top-level folders in your project:\n")
    for item in os.listdir(path):
        if os.path.isdir(item):
            print(f" - {item}/")

list_top_folders()
