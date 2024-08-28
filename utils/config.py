import os
from pathlib import Path

PROJECT_ROOT=Path(__file__).parent.parent.resolve()
UTILS_PATH = PROJECT_ROOT / "utils"
ASSIGNMENT_PATH = PROJECT_ROOT / "assignments"
REPORT_PATH = PROJECT_ROOT / "reports"\

BINARY_REPORT = REPORT_PATH / "Binary-Conversion-Report.txt"
HEX_REPORT = REPORT_PATH / "Hexadecimal-Conversion-Report.txt"
ASCII_REPORT = REPORT_PATH /"ASCII-Conversion-Report.txt"

SETTINGS = UTILS_PATH / "settings.json"

x = "CORRECT"
y = "INCORRECT"


def clear_screen():
    # For Unix/Linux
    if os.name == 'posix':
      os.system('clear')
    # For Windows
    elif os.name == 'nt':
      os.system('cls')

if __name__ == "__main__":
    print(PROJECT_ROOT)