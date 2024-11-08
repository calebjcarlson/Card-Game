import re
import time

# Establish arrays
encrypted_number = []
unencrypted_text = []
encrypted_text = []
salty = []
unsalty = []
salt1 = []
salt2 = []

# Letter to number dictionaries
letters = {'a':4,'b':14,'c':12,'d':25,'e':20,'f':10,'g':9,'h':5,'i':13,'j':1,'k':21,'l':17,'m':8,'n':22,'o':3,'p':16,'q':18,'r':2,'s':24,'t':26,'u':23,'v':19,'w':11,'x':15,'y':6,'z':7,' ':27}
normal_letters = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26,' ':27}

# Prompt user for what they want to do and as for salt
def prompt():
    user = input("Would you like to encrypt or decrypt? ")
    user_option = input_sanitizing(1, user)
    if user_option == 1:
        while True:
            salt = input("What would you like your salt value to be (Number 1-26)? ")
            print({salt})
            if re.search(r'^(?:[1-9]|1[0-9]|2[0-6])$', salt):
                return tonumber(salt)
            else:
                print("Not a valid input. Try again: ")
    elif user_option == 2:
        salt = input("What is the salt value of the encryption? (press enter if unsure) ")
        if re.search(r'^(?:[1-9]|1[0-9]|2[0-6])$', salt):
            fromletters(1, salt)
        else:
            fromletters(2, 0)
    else:
        print("\nSorry that is not a valid input\n")
        i = 0
        for i in range(15):
            print(" - ", end = '', flush=True)
            i += 1
            time.sleep(0.1)
        print("\n")
        prompt()


# Function used to sanitze multiple inputs
def input_sanitizing(type, input):
    if type == 1:
        encrypt_pattern = r"encrypt|1|first|one|\bcode|en"
        decrypt_pattern = r"decrypt|2|second|two|decode|de"
        if re.search(encrypt_pattern, input):
            return 1
        elif re.search(decrypt_pattern, input):
            return 2
        else:
            return 3
    elif type == 2:
        input = input.lower()
        if re.fullmatch(r"^[a-zA-Z ]+$", input):
            return(input)
        else:
            print("Not a valid text (only a-z allowed)\n")
            prompt()

# Converting text into numbers using the encrypted dictionary
def tonumber(salt):
    text = input("What is the text you would like to encrypt? ")
    text = input_sanitizing(2, text)
    for letter in text:
        for key, value in letters.items():
            if letter == key:
                number = value
                encrypted_number.append(number)
    salt = int(salt)
    harden(salt)

def etonumber(txt):
    for letter in txt:
        for key, value in normal_letters.items():
            if letter == key:
                number = value
                encrypted_number.append(number)

# Strengthen the encryption on the numbers
def harden(salt):
    psalt = salt
    for number in encrypted_number:
        salt1.append(salt)   
        if number == 27:
            salty.append(number)
            continue
        salted = number + salt
        if salted > 26:
            salted -= 26
        salty.append(salted)
        salt += salted
        if salt > 26:
            salt -= 26
    efromnumber(psalt)
            
# Take away the hardened encryption from the numbers    
def unharden(salt):
    for number in encrypted_number:
        salt2.append(salt)
        if number == 27:
            unsalty.append(number)
            continue
        unsalted = number - salt
        if unsalted <= 0:
            unsalted += 26
        unsalty.append(unsalted)
        salt += number
        if salt > 26:
            salt -= 26

# Decrypt from letters           
def fromletters(choice, salt):
    txt = input("What is the text you would like to decrypt?\n")
    txt = input_sanitizing(2, txt)
    salt = int(salt)
    etonumber(txt)
    if choice == 1:
        unharden(salt)
        fromnumber(salt)
    elif choice == 2:
        print("\n----------- Text could be one of these: -----------")
        for i in range(27):
            salt = i
            unharden(salt)
            fromnumber(salt)
            unsalty.clear()
            unencrypted_text.clear()
            i += 1

# Convert numbers back into readable text
def fromnumber(salt):
    for number in unsalty:
        for key, value in letters.items():
            if number == value:
                letter = key
                unencrypted_text.append(letter)
    print(f"Here is your unencrypted text (salt = {salt}):\n" + ''.join(unencrypted_text))

# Convert encrypted numbers into encrypted text
def efromnumber(psalt):
    psalt = psalt
    for number in salty:
        for key, value in normal_letters.items():
            if number == value:
                letter = key
                encrypted_text.append(letter)
    print(f"Here is the encrypted text using a salt value of {psalt} \n" + "".join(encrypted_text))


def main():
    prompt()
main()