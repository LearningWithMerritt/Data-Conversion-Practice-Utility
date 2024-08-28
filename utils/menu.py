import time
import base64

from utils.verify import *
from utils.config import *
import assignments.binary_conversion as binary
import assignments.hexadecimal_conversion as hexadecimal
import assignments.ascii_conversion as ascii



def start_menu(args):
    check_path()

    try:
        if sys.argv[1] == "hash":
            show_hashes()

        elif sys.argv[1] == "update":
            update_hashes()
            update_files()

        elif sys.argv[1] == "clear":
            
            for filename in os.listdir(REPORT_PATH):
                file_path = os.path.join(REPORT_PATH, filename)
                # Check if it's a file (not a subdirectory)
                if os.path.isfile(file_path):
                    os.remove(file_path)  
                    print(f"Deleted {file_path}")


    except IndexError as e:
        pass


    while(True):
        check_hash()
        check_path()

        print("\n@lwm:/$ Welcome to the Command Line Data Conversion Practice Utility.\n")
        try:
            choice = int(input("@lwm:/$ What would you like to do?\n1) Binary Conversion\n2) Hexadecimal Conversion\n3) ASCII Conversion\n4) See Report\n5) Start Assignment Over\n6) Exit\n").strip())
            clear_screen()

            if choice == 1:
                binary.main()
            
            elif choice == 2:
                hexadecimal.main()

            elif choice == 3:
                ascii.main()

            elif choice == 4:
                report_menu()

            elif choice == 5:
                restart_menu()
                
            elif choice == 6:
                exit()
            else:
                raise ValueError

        except ValueError as e:
            print("Please enter a valid number 1-6.\n")



def report_menu():
    files = os.listdir(REPORT_PATH)

    if len(files) < 1:
        input("There are no reports currently available.\nPress ENTER to continue.\n")
        clear_screen()
        return

    print("@lwm:/$ What report would you like to see?...")
    for i, file in enumerate(files):
        print(f"{i+1}) {file}")
        time.sleep(1)

    try:
        choice = int(input())

        with open(REPORT_PATH / files[choice-1], "rb") as report:
            content = report.read()
            content = base64.b64decode(content).decode('utf-8')
            print(content)

    except (ValueError,IndexError) as e:
        print(f"Please enter a valid number 1-{len(files)}.\n")

def restart_menu():

        try:
            choice = int(input("@lwm:/$ Which assignment would you like to start over?\n1) Binary Conversion\n2) Hexadecimal Conversion\n3) ASCII Conversion\n4) Exit\n"))

            with open(SETTINGS, "r") as file:
                data = json.load(file)

            if (choice == 1):
                data["binary_conversion_save"] = {}
            elif (choice == 2):
                data["hexadecimal_conversion_save"] = {}
            elif (choice == 3):
                data["ascii_conversion_save"] = {}
            elif (choice == 4):
                return
            else:
                raise ValueError
            
            with open(SETTINGS, 'w') as file:
                json.dump(data, file, indent=4)

        except ValueError as e:
            print("Please enter a valid number 1-4.\n")


