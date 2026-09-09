import random, re, base64, os, time, json, traceback
from datetime import datetime, timedelta
from getpass import getuser

APP_TITLE = "Data_Conversion_Practice_Utility"
SAVEFILE = "save.json"
LOGFILE = "error.log"
PROMPT_INDICATOR = "$> "

#UTILS

def wait():
    input("[ Press [ENTER] to continue... ]")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pad(string,desired_length,front=False):
    if len(string) < desired_length:
        num_spaces = desired_length - len(string)
        if(front):
            padded_string = " " * num_spaces + string
        else:
            padded_string = string + (" " * num_spaces)
    else:
        padded_string = string
    return padded_string

def log(data):
    with open(LOGFILE,"a") as f:
            f.write(f"{datetime.now()} : [ {data} ] \n")



class Menu:
    
    def __init__(self, prompt, options):
        '''
            key : (desciption, choice to return)
        '''
        self.prompt = prompt
        self.options = options

        


    def userin(self):
        choice = input(PROMPT_INDICATOR).strip().lower()
        while choice not in self.options.keys():
            clear()
            print("[ Please pick a valid option. ]")
            self.show()
            choice = input(PROMPT_INDICATOR).strip().lower()

        return choice

    def show(self):
        print(self.prompt)

        for key, (description, _ ) in self.options.items():
            print(f"{key}. {description}")

    def run(self):
        clear()
        self.show()
        choice = self.userin()
        return self.options[choice][1]

class Quiz:
    def __init__(self, qtype, nquestions, new_quiz = False):
        self.qtype = qtype
        self.nquestions = nquestions
        self.bank = {} 
        self.t0 = time.time()
        self.t_previous = 0
        self.history = {} # key : (question, response, accuracy)
        self.ncorrect = 0
        self.uname = ""
        self.new_quiz = new_quiz
        self.loaded = False

        self.init_data()
        

    def init_data(self):
        if "binary" == self.qtype:
            self.options = ("decimal", "binary")
            for decimal in range(256):
                binary = str(bin(decimal)[2:]).lstrip("0")

                # if len(binary) < 8:
                #     nspaces = 8 - len(binary)
                #     binary = ("0" * nspaces) + binary
                
                self.bank[str(decimal)] = binary
        
        elif "hexadecimal" == self.qtype:
            self.options = ("decimal","hexadecimal")
            for decimal in range(256):
                hexadecimal = str(hex(decimal)[2:]).lstrip("0")
                self.bank[str(decimal)] = hexadecimal
        
        elif "ascii" == self.qtype:
            # dec to char, bin to char, hex to char
            # char to dec, char to bin, char to hex
            self.options = ("decimal", "binary", "hexadecimal", "character")
            for decimal in range(32,127):
                binary = str(bin(decimal)[2:]).lstrip("0")
                hexadecimal = str(hex(decimal)[2:]).lstrip("0")
                character = chr(decimal)

                self.bank[str(decimal)] = (binary,hexadecimal,character)
        
        # elif "rgb" == self.qtype:
        #     # dec rgb to color; color to dec rgb
        #     # hex rgb to color; color to hex rgb
        #     self.rgb = {
        #         "black":   [(0, 0, 0), "000000"],
        #         "red":     [(255, 0, 0), "FF0000"],
        #         "green":   [(0, 255, 0), "00FF00"],
        #         "blue":    [(0, 0, 255), "0000FF"],
        #         "gray" :   [(128, 128, 128), "808080"],
        #         "yellow":  [(255, 255, 0), "FFFF00"],
        #         "magenta": [(255, 0, 255), "FF00FF"],
        #         "cyan":    [(0, 255, 255), "00FFFF"],
        #         "white":   [(255, 255, 255), "FFFFFF"]
        #     }

    def get_uname(self):

        try:
            self.uname = getuser().upper()
            print(f"{datetime.now()} : [ Username Set : {self.uname}]")
            time.sleep(0.5)
        except:
            uname = input("[ Please type your first and last name then hit [ENTER] ]\n")
            pattern = r"[a-zA-Z]+\s[a-zA-Z]+"
            match = re.fullmatch(pattern, uname)
            while not match:
                clear()
                uname = input("[ Please type your first and last name then hit [ENTER] ]\n")
                match = re.fullmatch(pattern, uname)
        
            self.uname = uname
            print(f"{datetime.now()} : [ Username Set : {self.uname}]")
            
            tryagain = input("[ Would you like to edit your username? (y) OR Press [ENTER] to continue...]").strip().lower()
            if(tryagain == "y"):
                clear()
                self.get_uname()
        
    def load(self):
        try: 

            with open("json.save", "rb") as f:
                encoded = f.read()
            
            data = json.loads(base64.b64decode(encoded).decode("utf-8"))


            if(f"{self.qtype}_save" in data.keys()):
                self.uname = data.get(f"{self.qtype}_save").get("uname")
                self.t_elapsed = self.t_previous = data.get(f"{self.qtype}_save").get("t_elapsed")
                self.ncorrect = data.get(f"{self.qtype}_save").get("ncorrect")
                self.history = data.get(f"{self.qtype}_save").get("history")

                for key in self.history.keys():
                    if key in self.bank:
                        self.bank.pop(key)

                print(f"{datetime.now()} : [ PREVIOUS RESPONSES FOUND AND LOADED ]\n")
                time.sleep(1)

                self.t0 = time.time()
                self.loaded = True
            else:
                self.save()

        except FileNotFoundError as e:
            log("No previous save file found")
            print(f"{datetime.now()} : [ No previous save file found. ]")
            # with open(SAVEFILE, "w"):
            #     pass

            with open("json.save","w"):
                pass

            self.save()

            log("json.save file created successfully")
        
        except json.JSONDecodeError as e:
            log(str(e))
            self.save()
            return

        except KeyboardInterrupt:
            raise

        except Exception as e:
            log(f"Unable to load save data --> {e}")
            print(f"{datetime.now()} : [ Unable to load save data. ]")

            raise

    def save(self):
        try:
            if self.uname == "":
                self.get_uname()
            self.t_elapsed = (time.time() - self.t0) + self.t_previous

            with open("json.save", "rb") as f:
                    encoded = f.read()
            try:
                data = json.loads(base64.b64decode(encoded).decode("utf-8"))

            except json.decoder.JSONDecodeError as e:
                data = {}

            data[f"{self.qtype}_save"] = {
                "uname" : self.uname,
                "t_elapsed"  : self.t_elapsed,
                "ncorrect" : self.ncorrect, 
                "history" : self.history
                }

            # with open(SAVEFILE, "w") as file:
            #     json.dump(data, file, indent=4)

            encoded = base64.b64encode(json.dumps(data).encode("utf-8"))
            with open("json.save", "wb") as f:
                f.write(encoded)

        except KeyboardInterrupt:
            raise

        except FileNotFoundError:
            log(f"{SAVEFILE} not found while attempting to save.")
            with open("json.save", "w") as f:
                pass

        except Exception as e:
            log(f"An error occured while saving answers. --> {e}")
            print(f"[ An error occured while saving answers. ]\n{e}")
    
    def run(self):

        if self.new_quiz:
            self.save()
            self.loaded = False
        else:
            try:
                self.load()
                if (len(self.history) >= self.nquestions):
                    self.report()
                    return
            except:
                pass

        if self.uname == "":
            self.get_uname()

        clear()
        directions = (
            "[ Directions: ]\n"
            "[ You will be presented with randomly generated conversion questions. ]\n"
            "[ After you answer all of the questions, your work will be autograded and a report generated. ]\n" 
        )

        print(directions)
        input("[ Press [ENTER] to continue... ]\n")


        while len(self.history) < self.nquestions:
            key = random.choice(list(self.bank.keys()))

            qdata = {
                "decimal" : key
            }

            if "ascii" == self.qtype:
                qdata.update({
                    "binary" : self.bank.get(key)[0],
                    "hexadecimal": self.bank.get(key)[1],
                    "character": self.bank.get(key)[2],
                })
            else:
                qdata[self.qtype] = self.bank.get(key)


            convert_from, convert_to = random.sample(self.options, 2)

            if self.qtype == "ascii":
                while convert_from != "character" and convert_to != "character":
                    convert_from, convert_to = random.sample(self.options, 2)

        
            hudbar = (f"[ USER: {self.uname} | QUIZ: {self.qtype} | # CORRECT: {self.ncorrect} | QUESTION #: {len(self.history)+1}/{self.nquestions} ]")

            qprompt = f"[ {len(self.history)+1}.) Convert {convert_from} '{qdata.get(convert_from)}' to {convert_to} ]:\n"

            qanswer = qdata.get(convert_to)
            
            question = Question(
                hudbar,
                qprompt,
                qanswer,
                convert_to
                )
            qresponse = question.userin()
            accurate = question.check_answer()
            if("\u2705 CORRECT" == accurate): self.ncorrect += 1

            self.history[key] = (qprompt.replace("\n",""),qresponse,accurate, qanswer)
            self.bank.pop(key)
            time.sleep(1)
            
            self.save()

        self.report()

    def report(self):
        if not self.loaded:
            self.load()


        percent = self.ncorrect / self.nquestions * 100

        if percent > 75:
            unicode = "\u2705"
        else:
            unicode = "\u2757"

        header = (
            f"[ USER: {self.uname} | QUIZ: {self.qtype} | ELAPSED TIME: {timedelta(seconds = int(self.t_elapsed))} |" +
            f" TOTAL CORRECT: {self.ncorrect}/{self.nquestions} {unicode} | PERCENT CORRECT: {percent}% {unicode} ]"
        )

        clear()
        print("-" * len(header))
        print(header, end = "\n\n")


        n = 1
        longest = [0,0,0,0]

        rows = list(self.history.values())
        rows.insert(0,["Question", "Response", "\u2705 Accuracy", "Correct Answer"])

        for record in rows:
            if len(record[0]) > longest[0]: longest[0] = len(record[0])
            if len(record[1]) > longest[1]: longest[1] = len(record[1])
            if len(record[2]) > longest[2]: longest[2] = len(record[2])
            if len(record[3]) > longest[3]: longest[3] = len(record[3])

    
        for record in rows:
            line =(
                "| " + pad(record[2],longest[2]) + " | " +
                pad(record[0],longest[0]) + " | " +
                pad(record[1],longest[1]) + " | " +
                pad(record[3],longest[3]) + " | "
                
            )

            print(line)
            n += 1
        print("-" * len(header))
        print()
        wait()

class Question:

    def __init__(self,hud:str, prompt:str, answer:str, answer_type:str):
        self.hud = hud
        self.prompt = prompt + f"\n[ Type your answer below and hit [ENTER] to submit. ]\n{PROMPT_INDICATOR}"
        self.answer = answer
        self.answer_type = answer_type
        self.set_pattern()


    def userin(self):
        clear()

        print(self.hud)
        self.user_response = input(self.prompt).lower().strip()

        # handle all zero pattern --> r"0+"
        if re.fullmatch(r"0+", self.user_response):
            self.user_response = "0"
        else:
            self.user_response.lstrip("0")


        if self.answer_type in ["decimal", "binary", "hexadecimal"]:
            # self.answer = self.answer.lstrip("0")
            if self.user_response[:2] in ["0x","0b"]:
                self.user_response = self.user_response[2:]
            self.user_response = self.user_response.lstrip("0")

        match = re.fullmatch(self.pattern, self.user_response)
        while not match:
            clear()
            print(self.invalid_response)
            input("[ Press [ENTER] to continue... ]")
            clear()

            print(self.hud)
            self.user_response = input(self.prompt).lower().strip()

            if re.fullmatch(r"0+", self.user_response):
                self.user_response = "0"
            else:
                self.user_response.lstrip("0")

            match = re.fullmatch(self.pattern, self.user_response)

        return self.user_response

    def check_answer(self) ->  bool:
        if self.user_response == self.answer:
            print("\u2705 CORRECT")
            return "\u2705 CORRECT"
        else:
            print("\u274C INCORRECT")
            return "\u274C INCORRECT"

    def set_pattern(self):
        '''Answer pattern is determined by the answer type'''
        '''Invalid response is determined by the answer type'''
        match self.answer_type:

            case "decimal":
                self.pattern = r"^[0-9]{1,4}$"
                self.invalid_response = (
                    "Your answer should be a decimal number containing only digits 0-9 between the values of 0-1000, with no extra spaces"
                )

            case "binary":
                self.pattern = r"^[0-1]{1,8}$"
                self.invalid_response = (
                    "Your answer should be a binary number containing only 0s and 1s no longer than a byte (8bits), with no extra spaces"
                )
            
            case "hexadecimal":
                self.pattern = r"^[0-9A-Fa-fxX#]{1,4}$"
                self.invalid_response = (
                    "Your answer should be a hexadecimal number containing digits 0-9 A-F between 00 and FF, with no extra spaces"
                )
            
            case "character":
                self.pattern = r"^.$"
                # self.pattern = r"^\S{1}$"
                self.invalid_response = "Your answer should be a single character, with no extra spaces"
            
            case _:
                self.pattern = None
            
class App:
    def __init__(self):
        self.running = True
        self.menu_stack = ["main"]
        self.welcome = "[ @lwm:/$ Welcome to the Command Line Data Conversion Practice Utility. ]\n"
        self.set_menus()

        self.run()

    def run(self):
        while self.running:
            current = self.menu_stack[-1]
            menu = self.menus[current]


            choice = menu.run()

            match choice:
                case "quit":
                    self.running = False
                case "back":
                    if len(self.menu_stack) > 1:
                        self.menu_stack.pop()

                case "load":
                        Quiz(current,25).run()
                case "new":
                        Quiz(current,25,True).run()
                case "report":
                        Quiz(current,25).report()
                case _ :
                    if choice in self.menus.keys():
                        self.menu_stack.append(choice)

                    else:
                        print(["[ Please select a valid option. ]"])
                        time.sleep(0.5)

    def set_menus(self):

        quiz_menu = Menu(
                "[ What would you like to do? ]:\n",
                {
                    "1" : ("Load Previous", "load"),
                    "2" : ("Start New", "new"),
                    "3" : ("Show Report","report"),
                    "b" : ("Back", "back"),
                    "q" : ("Quit", "quit")
                }
        )

        self.menus = {
            "main" : Menu(
                f"{self.welcome}[ Pick the quiz you would like to take. ]:\n",
                {
                    "1" : ("Binary Quiz", "binary"),
                    "2" : ("Hexadecimal Quiz", "hexadecimal"),
                    "3" : ("ASCII Quiz", "ascii"),
                    "q" : ("Quit", "quit")
                }, 
            ),
            "binary" : quiz_menu,
            "hexadecimal" : quiz_menu,
            "ascii" : quiz_menu
        }       


   

if __name__ == "__main__":
    try:
        App()
    except KeyboardInterrupt:
        clear()
        print("GOODBYE!")
        time.sleep(1)




