'''ASCII Conversion Questions generator'''

'''
note:
student error with saved json data getting more correct than possible
name regex will allow " characters
'''

import random,re,base64,os,time,json,re
from utils.config import *

correct_num = int("00",16)
total_num = int("1e",16)
bin_ascii = {}
ascii_bin = {}
hex_ascii = {}
student_answers = {}
encoding = ("binary", "ASCII", "hexadecimal")
directions = """
Directions: 
  You will be presented with randomly generated conversion questions.
  After you answer all the questions, your work will be autograded and a report generated.
"""
question_directions = " Type your answer and hit enter or Type 'exit' to quit. : \n"


def create_bin2ascii_pair():
  for decimal in range(32,127):
    binary = bin(decimal)[2:]
    letter = chr(decimal)
    bin_ascii[str(binary)] = letter

def create_ascii2bin_pair():
  for key in bin_ascii:
    ascii_bin[bin_ascii[key]] = key

def create_hex2ascii_pair():
  for decimal in range(32,127):
    hexa = hex(decimal)
    letter = chr(decimal)
    hex_ascii[str(hexa)] = letter

def create_question():
  global correct_num,student_answers
  response = load_responses()
  correct_num = response[0]
  student_answers = response[1]
  # print("correct_num before: ", correct_num)
  while len(student_answers) < total_num:
    switch = random.randint(0,2)
    if(switch == 0):
      key = random.choice(list(bin_ascii.keys()))
      
      ascii_char = bin_ascii[key]
      # print(ascii_char)
      question = (f"{len(student_answers)+1}) Convert {encoding[0]} {key} to {encoding[1]}.")
      answer = input(f"\n{question}"+ question_directions)

      if(answer.lower().strip() == "exit"):
        return
      
      if ascii_char != " ":
        pattern = r"^\S{1}$"
        match = re.search(pattern,answer)
        while not match:
          os.system('cls' if os.name == 'nt' else 'clear')
          print("Your answer should be a single character, with no extra spaces")
          answer = input(f"{question}"+ question_directions)
          match = re.search(pattern,answer)
    
      if answer == ascii_char:
        check = x
        print(check)
        correct_num += 1
      else:
        check = y
        print(check)
      student_answers[question] = (answer,ascii_char,check)
      bin_ascii.pop(key)
    elif(switch == 1):
      key = random.choice(list(ascii_bin.keys()))

      binary_num = ascii_bin[key]
      question = (f"{len(student_answers)+1}) Convert {encoding[1]} {key} to {encoding[0]}.")
      # print(binary_num)
      answer = input(f"\n{question}" + question_directions)

      if(answer.lower().strip() == "exit"):
        return

      pattern = r"^[0-1]{1,8}$"
      match = re.search(pattern,answer)
      while not match:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Your answer should be a binary number containing only 0s and 1s, with no extra spaces")
        answer = input(f"{question}"+ question_directions)
        match = re.search(pattern,answer)

      all_zero_pattern = r"0+"
      all_zero_match = re.fullmatch(all_zero_pattern, answer)
      if all_zero_match:
        answer = "0"
      else:
        answer = answer.lstrip("0")

      if answer == binary_num:
        check = x
        print(check)
        correct_num += 1
      else:
        check = y
        print(check)
      student_answers[question] = (answer,binary_num,check)
      ascii_bin.pop(key)
    else:
      key = random.choice(list(hex_ascii.keys()))

      ascii_char = hex_ascii[key]
      question = (f"{len(student_answers)+1}) Convert {encoding[2]} {key} to {encoding[1]}.")
      # print(ascii_char)
      answer = input(f"\n{question}" + question_directions)

      if(answer.lower().strip() == "exit"):
        return

      if ascii_char != " ":
        pattern = r"^\S{1}$"
        match = re.search(pattern,answer)
        while not match:
          os.system('cls' if os.name == 'nt' else 'clear')
          print("Your answer should be a single character, with no extra spaces")
          answer = input(f"{question}"+ question_directions)
          match = re.search(pattern,answer)
    
      if answer == ascii_char:
        check = x
        print(check)
        correct_num += 1
      else:
        check = y
        print(check)
      student_answers[question] = (answer,ascii_char,check)
      hex_ascii.pop(key)
    # print("correct_num after: ", correct_num)
    track_answers()

def pad(string,desired_length,front):
  if len(string) < desired_length:
    num_spaces = desired_length - len(string)
    if(front):
      padded_string = " " * num_spaces + string
    else:
      padded_string = string + (" " * num_spaces)
  else:
    padded_string = string
  return padded_string

def gen_report():
  global name,elapsed_t
  try:
    os.remove(ASCII_REPORT)
  except FileNotFoundError as e:
    print("Generating Report...")
  percent = correct_num / total_num * 100
  with open(ASCII_REPORT, "w") as f:
    text = f"Name: {name}\nYour Results: {correct_num}/{total_num} | Percent Correct: {percent:.2f}%\nElapsed Time : {elasped_t}s\n"
    f.write(text +"\n")
    print("\n" + text)
    number = 1
    for key in student_answers.keys():
      value = student_answers[key]
      text = pad(f"Q{number})",4,False) + f" {pad(value[2],10,True)} | {pad(key,40,False)} | Your answer: {pad(str(value[0]),8,False)} | Correct answer: {pad(str(value[1]),8,False)} |"
      f.write(text + "\n")
      print(text)
      number += 1
  
  with open(os.path.join(os.path.dirname(__file__),ASCII_REPORT),"rb") as f:
    content = f.read()
  encoded = base64.b64encode(content)

  with open(os.path.join(os.path.dirname(__file__),ASCII_REPORT),"wb") as f:
    f.write(encoded)

def track_answers():
    try:
        with open(SETTINGS, "r") as file:
            data = json.load(file)

        data["ascii_conversion_save"] = {"n": correct_num, "answers": student_answers}

        with open(SETTINGS, 'w') as file:
            json.dump(data, file, indent=4)

    except Exception as e:
       print(f"Error occured while saving answers.\n{e}")

def load_responses():
    try:
        with open(SETTINGS, "r") as file:
            data = json.load(file)

        n_correct = data["ascii_conversion_save"]["n"]
        responses = data["ascii_conversion_save"]["answers"]
        remove_keys()
        print("PREVIOUS RESPONSES FOUND AND LOADED...\n")
        time.sleep(1)
    except:
        n_correct = 0
        responses = {}
    return (n_correct, responses)  

def remove_keys():
  for key in student_answers.keys():
    if key in bin_ascii:
      bin_ascii.pop(key)
    if key in ascii_bin:
      ascii_bin.pop(key)

def main():
  global name, elasped_t
  start_t = time.time()
  print(directions)
  name = input("Please type your first and last name then hit enter: ")
  pattern = r"[a-zA-Z]+\s[a-zA-Z]+"
  match = re.search(pattern, name)
  while not match:
    name = input("Invalid name.\nPlease type your first and last name then hit enter: ")
    match = re.search(pattern, name)
  create_bin2ascii_pair()
  create_ascii2bin_pair()
  create_hex2ascii_pair()
  create_question()
  end_t = time.time()
  elasped_t = end_t - start_t
  elasped_t = f"{elasped_t:.2f}"
  gen_report()










