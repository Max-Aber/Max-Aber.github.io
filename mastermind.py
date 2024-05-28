import random

def create_key():
    ltts = ['R','G','B','Y','P','O']
    code = ""
    for _ in range(4):
        c = random.choice(ltts)
        code += c
    return code


def new_guess(gc):
    valid = False 
    
    while not valid:
        valid = False
        guess = input(f"Enter guess ({gc}): ")
        guess = guess.replace(" ","").upper() #checks if its 4 letters
        if len(guess) == 4:
            valid = True
        else:
            print("Invalid: Guess is only 4 letters")
            continue
        
        g_letters = []
        for l in guess:
            g_letters.append(l)
        
        for let in g_letters:
            if let not in ['R','G','B','Y','P','O']: 
                valid = False
                print("Invalid: Colors not available")
                break                # checks if there are any invalid characters
            else:
                valid = True
                
    return guess


def check(guess, key):
    right_pos = []
    right_let = []
    guess_let = [l for l in guess]
    key_let = [l for l in key]
    for i in range(4):
        if guess[i] == key_let[i]:
            right_pos.append(guess[i])#checks corrects positions
            key_let[i] = "x"
            guess_let[i] = "v"
            
    for i in range(4):        
        if guess[i] in key_let:
            j = key_let.index(guess[i])#checks correct letters wrong position
            right_let.append(guess[i])
            guess_let[i] = "v"
            key_let[j] = "x"

    return (len(right_pos), len(right_let))

def play():
    play = True
    while play:
        won = False
        av_guesses = int(input("Number of attempts (8-12): "))
        key = create_key()
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
            print("Congratulations you Won!")#give congratulation or loss message
        else:
            print("Loss! You ran out of Tries")
        print("The key was:",key)
        
        y_or_n = input("would you like to play again(y/n)? ")
        while y_or_n.lower() not in ['y', 'n']:
            y_or_n = input("would you like to play again(y/n)? ")
            
        if y_or_n.lower() == 'y':
            play = True
        elif y_or_n.lower() == 'n':
            play = False

def main():
    print("WELCOME TO MASTERMIND")
    print("---------------------")
    
    print("Instructions ----- 1\nPlay ------------- 2")
    opt = input("Choice (1|2): ")
    while opt in [1,2]:
        opt = input("Choice (1|2): ")
    
    if opt == "1":
        print("Try to guess the 4 color code in both order and color within 8 to 12 attempts. ")
        print("There are 6 colors, Blue(B), Green(G), Orange(O), Purple(P), Red(r), Yellow(Y).")
        print("After your guess, you will know the number of correct guesses and correct letters\n")
        play()
        
    elif opt == "2":
        play()
        

main()