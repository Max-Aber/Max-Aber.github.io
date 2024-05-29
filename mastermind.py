import random
"""
DESCRIPTION:
This is a code solving game where you have to guess the
4 color code made out of the 6 colors, R,G,B,Y,P, or O.
After your guess you will see the amount of letters in your
guess that are in the right position and how many are in 
the code but not in the right spot.
"""

def create_key() -> str:
    """
    Creates a random code out of the letters R,G,B,Y,P, and O
    Returns:
        str: the code that is 4 letters
    """
    
    ltts = ['R','G','B','Y','P','O']
    code = ""   # make a random code of 4 out of the 6 letters
    for _ in range(4):
        c = random.choice(ltts)
        code += c
    return code


def new_guess(gc: int) -> str:
    """
    Gets a new guess and checks if it is valid
    
    Parameter:
        gc (int): the guess number
    Returns:
        str: The valid guess
    """
    valid = False 
    
    while not valid:
        guess = input(f"Enter guess ({gc}): ")
        valid = True
        guess = guess.replace(" ","").upper() # remove any white space and capitalize
        if len(guess) != 4: #checks if the right size
            valid = False
            print("Invalid: Guess is only 4 letters")
            continue
        
        for let in guess:   # checks if there are any invalid characters
            if let not in ['R','G','B','Y','P','O']: 
                valid = False
                print("Invalid: Colors not available")
                break                
    return guess


def check(guess: str, key: str) -> tuple[int, int]:
    """
    Checks for the amount of letters in the corrects spot and 
    the ones that are in the code but not in the right place
    
    Parameters:
        guess (str): the valid guess given by the player
        key (str): the correct key to compare the guess
    Returns:
        tuple: returns the amount of letters in the right spot and
        the ones in the code not in the right spot
    """
    right_pos = 0
    right_let = 0   # set up variables
    guess_let = [l for l in guess]
    key_let = [l for l in key]
    
    for i in range(4):
        if guess[i] == key_let[i]:
            right_pos += 1 #checks corrects positions
            key_let[i] = "x" 
            guess_let[i] = "v"
    # change to x or v so that it does not repeat in the right letters
    
    for i in range(4):        
        if guess[i] in key_let:
            j = key_let.index(guess[i])  #checks correct letters wrong position
            right_let += 1
            key_let[j] = "x"
            guess_let[i] = "v"

    return (right_pos, right_let) # returns number of right position and right letters

def play(av_guesses: int)-> None:
    """
    runs the game
    
    Parameters: 
        av_guesses (int): the amount of guesses given to the player
    """
    won = False
    key = create_key() # create variables and key
    guess_count = 0
    
    while av_guesses > guess_count and not won:
        guess_count += 1
        guess = new_guess(guess_count)
        r_pos, r_let = check(guess, key)
        #compare answers
        if (key == guess):
            won = True
            break
        
        print(f"{guess}: Correct possition: {r_pos} | Correct letter: {r_let}")
        # return which is in the right positions which not
    
    if won:
        print("Congratulations you Won!")
    else: #give congratulation or loss message
        print("Loss! You ran out of Tries")
    print("The key was:",key)
        

def main():
    print("WELCOME TO MASTERMIND")
    print("---------------------")
    
    print("Instructions ----- 1\nPlay ------------- 2")
    opt = input("Choice (1|2): ")
    while opt not in ('1','2'):
        opt = input("Choice (1|2): ")
    
    if opt == "1":
        print("Try to guess the 4 color code in both order and color within 8 to 12 attempts. ")
        print("There are 6 colors, Blue(B), Green(G), Orange(O), Purple(P), Red(r), Yellow(Y).")
        print("After your guess, you will know the number of correct guesses and correct letters\n")    
        
    do_play = True
    while do_play:
        available_guesses = int(input("Number of attempts (8-12): "))
        while available_guesses not in range(8, 13):    # get number of tries
            available_guesses = int(input("Number of attempts (8-12): "))
        play(available_guesses)
        
        y_or_n = input("would you like to play again(y/n)? ")
        while y_or_n.lower() not in ['y', 'n']: # ask if you want to play again
            y_or_n = input("would you like to play again(y/n)? ")
            
        if y_or_n.lower() == 'n':
            do_play = False
            print("Thank you for playing!")
        

main()