'''Hexadecimal Converstion Questions generator'''

import random, re, base64, os, time, json
from utils.config import *

correct_num = int("00", 16)
total_num = int("1e", 16)
decimal_hex = {}
hex_decimal = {}
student_answers = {}
encoding = ("decimal", "hexadecimal")
directions = """
Directions: 
  You will be presented with randomly generated conversion questions.
  After you answer all the questions, your work will be autograded and a report generated.
"""
question_directions = " Type your answer and hit enter or Type 'exit' to quit. : \n"


def create_dec2hex_pair():
  for decimal in range(256):
    hexadecimal = hex(decimal)[2:]
    decimal_hex[str(decimal)] = hexadecimal.upper()


def create_hex2dec_pair():
  for key in decimal_hex:
    hex_decimal[decimal_hex[key]] = key


def create_question():
  global correct_num, student_answers
  response = load_responses()
  correct_num = response[0]
  student_answers = response[1]

  while len(student_answers) < total_num:
    switch = random.randint(0, 1)
    if (switch):
      key = random.choice(list(decimal_hex.keys()))

      hex_num = decimal_hex[key]
      question = (
        f"{len(student_answers)+1}) Convert {encoding[0]} {key} to {encoding[1]}."
      )
      answer = input(f"\n{question}" + question_directions)

      if(answer.lower().strip() == "exit"):
        return

      pattern = r"^[0-9A-Fa-fxX#]{1,4}$"
      match = re.search(pattern, answer)
      while not match:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
          "Your answer should be a hexadecimal number containing digits 0-9 A-F between 00 and FF, with no extra spaces"
        )
        answer = input(f"{question}" + question_directions)
        match = re.search(pattern, answer)
      
      answer = answer.upper()

      if answer.startswith("0X"):
        answer = answer[2:]
      elif answer.startswith("#") or answer.startswith("X"):
        answer = answer[1:]

      all_zero_pattern = r"0+"
      all_zero_match = re.fullmatch(all_zero_pattern, answer)
      if all_zero_match:
        answer = "0"
      else:
        answer = answer.lstrip("0")

      if answer == hex_num:
        check = x
        print(check)
        correct_num += 1
      else:
        check = y
        print(check)
      student_answers[question] = (answer, hex_num, check)
      decimal_hex.pop(key)
    else:
      key = random.choice(list(hex_decimal.keys()))

      decimal_num = hex_decimal[key]
      question = (
        f"{len(student_answers)+1}) Convert {encoding[1]} 0x{key} to {encoding[0]}."
      )
      answer = input(f"\n{question}" + question_directions)
    
      if(answer.lower().strip() == "exit"):
        return

      pattern = r"^[0-9]{1,4}$"
      match = re.search(pattern, answer)
      while not match:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
          "Your answer should be a decimal number containing only digits 0-9 between the values of 0-1000, with no extra spaces"
        )
        answer = input(f"{question}" + question_directions)
        match = re.search(pattern, answer)

      all_zero_pattern = r"0+"
      all_zero_match = re.fullmatch(all_zero_pattern, answer)
      if all_zero_match:
        answer = "0"
      else:
        answer = answer.lstrip("0")

      if answer == decimal_num:
        check = x
        print(check)
        correct_num += 1
      else:
        check = y
        print(check)
      student_answers[question] = (answer, decimal_num, check)
      hex_decimal.pop(key)

    track_answers()


def pad(string, desired_length, front):
  if len(string) < desired_length:
    num_spaces = desired_length - len(string)
    if (front):
      padded_string = " " * num_spaces + string
    else:
      padded_string = string + (" " * num_spaces)
  else:
    padded_string = string
  return padded_string


def gen_report():
  global name, elapsed_t
  try:
    os.remove(BINARY_REPORT)
  except FileNotFoundError as e:
    print("Generating Report...")
  percent = correct_num / total_num * 100
  with open(HEX_REPORT, "w") as f:
    text = f"Name: {name}\nYour Results: {correct_num}/{total_num} | Percent Correct: {percent}%\nElapsed Time : {elasped_t}s\n"
    f.write(text + "\n")
    print("\n" + text)
    number = 1
    for key in student_answers.keys():
      value = student_answers[key]
      text = pad(
        f"Q{number})", 4, False
      ) + f" {pad(value[2],10,True)} | {pad(key,40,False)} | Your answer: {pad(str(value[0]),8,False)} | Correct answer: {pad(str(value[1]),8,False)} |"
      f.write(text + "\n")
      print(text)
      number += 1

  with open(os.path.join(os.path.dirname(__file__), HEX_REPORT),
            "rb") as f:
    content = f.read()
  encoded = base64.b64encode(content)

  with open(os.path.join(os.path.dirname(__file__), HEX_REPORT),
            "wb") as f:
    f.write(encoded)


def track_answers():
    try:
        with open(SETTINGS, "r") as file:
            data = json.load(file)

        data["hexadecimal_conversion_save"] = {"n": correct_num, "answers": student_answers}

        with open(SETTINGS, 'w') as file:
            json.dump(data, file, indent=4)

    except Exception as e:
       print(f"Error occured while saving answers.\n{e}")


def load_responses():
    try:
        with open(SETTINGS, "r") as file:
            data = json.load(file)

        n_correct = data["hexadecimal_conversion_save"]["n"]
        responses = data["hexadecimal_conversion_save"]["answers"]
        remove_keys()
        print("PREVIOUS RESPONSES FOUND AND LOADED...\n")
        time.sleep(1)
    except:
        n_correct = 0
        responses = {}
    return (n_correct, responses)  


def remove_keys():
  for key in student_answers.keys():
    if key in decimal_hex:
      decimal_hex.pop(key)
    if key in hex_decimal:
      hex_decimal.pop(key)


def main():
  global name, elasped_t
  start_t = time.time()
  print(directions)
  name = input("Please type your first and last name then hit enter: ")
  pattern = r"[a-zA-Z]+\s[a-zA-Z]+"
  match = re.search(pattern, name)
  while not match:
    name = input(
      "Invalid name.\nPlease type your first and last name then hit enter: ")
    match = re.search(pattern, name)
  create_dec2hex_pair()
  create_hex2dec_pair()
  create_question()
  end_t = time.time()
  elasped_t = end_t - start_t
  elasped_t = f"{elasped_t:.2f}"
  gen_report()

