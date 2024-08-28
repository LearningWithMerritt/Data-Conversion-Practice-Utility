import hashlib
import os, sys
import json
import base64

import time

from utils.config import *


def get_hash(path, print_out=False):
    hasher = hashlib.sha256()

    with open(path,'rb') as f:
        while True:
            data = f.read(65536)

            if not data:
                break
            hasher.update(data)

    hash_value = hasher.hexdigest()

    if(print_out):
        print(hash_value)

    return(hash_value)


def show_hashes():

    files = os.listdir(PROJECT_ROOT / "assignments")

    for file in files:
        print(f"{file}: {get_hash(PROJECT_ROOT / "assignments" / file)}")


def check_hash():

    try:
        with open(PROJECT_ROOT/ "utils" / "settings.json", "r") as file:
            data = json.load(file)

        if (data["binary_conversion_assignment_hash"] == get_hash(PROJECT_ROOT / "assignments" / "binary_conversion.py") and
            data["hexadecimal_conversion_assignment_hash"] == get_hash(PROJECT_ROOT / "assignments" / "hexadecimal_conversion.py") and
            data["ascii_conversion_assignment_hash"] == get_hash(PROJECT_ROOT / "assignments" / "ascii_conversion.py")
        ):
           return
        else:
            print("SETTING FILES")
            set_files()

    except Exception as e:
       print(f"An Error Occured\n{e}")
       exit()

def check_path():
    if not os.path.exists(REPORT_PATH):
        os.makedirs(REPORT_PATH)

def update_hashes():
    data = {}
    try:
        with open(PROJECT_ROOT/ "utils" / "settings.json", "r") as file:
            data = json.load(file)
    except Exception as e:
       pass

    data["binary_conversion_assignment_hash"] = get_hash(PROJECT_ROOT / "assignments" / "binary_conversion.py")
    data["hexadecimal_conversion_assignment_hash"] = get_hash(PROJECT_ROOT / "assignments" / "hexadecimal_conversion.py")
    data["ascii_conversion_assignment_hash"] = get_hash(PROJECT_ROOT / "assignments" / "ascii_conversion.py")

    with open(PROJECT_ROOT/ "utils" / "settings.json", 'w') as file:
      json.dump(data, file, indent=4)

def update_files():
        try:
            with open(SETTINGS, "r") as file:
                data = json.load(file)

            
            files = os.listdir(ASSIGNMENT_PATH)
            for filename in files:
                path = os.path.join(ASSIGNMENT_PATH,filename)
                if os.path.isfile(path):
                    with open(ASSIGNMENT_PATH / filename,"rb") as f:
                        encoded = base64.b64encode(f.read()).decode("utf-8")
                    
                    data[filename] = encoded

            with open(SETTINGS, 'w') as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"An Error Occurred while updating file backups.\n{e}")

def set_files():
    try:
        with open(SETTINGS, "r") as file:
            data = json.load(file)

        for key in data:
            if ".py" in key:
                with open(ASSIGNMENT_PATH / key, "wb") as filename:
                    filename.write(base64.b64decode(data[key]))

    except Exception as e:
        print(f"An error occurred while writing to files.\n{e}")

        
    #     try:
    #         with open(ASSIGNMENT_PATH / "binary_conversion_assignment.py", "r") as file:
    #             content = file.read()

    #     try:
        
    #     with open(SETTINGS, "r") as file:
    #         data = json.load(file)

    #     data["binary_conversion_backup"] = 

    #     with open(SETTINGS, 'w') as file:
    #         json.dump(data, file, indent=4)

    # except Exception as e:
    #    print(f"Error occured while saving answers.\n{e}")

























