import sys

braille_to_english = {
    'O.....': 'A', 'O.O...': 'B', 'OO....': 'C', 'OO.O..': 'D', 'O..O..': 'E',
    'OOO...': 'F', 'OOOO..': 'G', 'O.OO..': 'H', '.OO...': 'I', '.OOO..': 'J',
    'O...O.': 'K', 'O.O.O.': 'L', 'OO..O.': 'M', 'OO.OO.': 'N', 'O..OO.': 'O',
    'OOO.O.': 'P', 'OOOOO.': 'Q', 'O.OOO.': 'R', '.OO.O.': 'S', '.OOOO.': 'T',
    'O...OO': 'U', 'O.O.OO': 'V', '.OOO.O': 'W', 'OO..OO': 'X', 'OO.OOO': 'Y',
    'O..OOO': 'Z',
    '......': ' ',  # space
    '.O....': 'Capital',  # capitalized
    '.O.O..': 'Number'  # number
}

english_to_braille = {v: k for k, v in braille_to_english.items()}

number_mapping = {
    'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5',
    'F': '6', 'G': '7', 'H': '8', 'I': '9', 'J': '0'
}

def braille_to_text(braille):
    result = []
    i = 0
    capitalize_next = False
    number_mode = False

    while i < len(braille):
        symbol = braille[i:i+6]
        
        if symbol == '.O....':  #capital 
            capitalize_next = True
        elif symbol == '.O.O..':  #number 
            number_mode = True
        else:
            char = braille_to_english.get(symbol, '')
            
            # If we're in number mode and the character is A-J, we convert it to a number
            if number_mode and char in 'ABCDEFGHIJ':
                char = number_mapping[char]
            elif char == ' ':
                # A space turns off number mode
                number_mode = False  
            
            # If we saw a capital symbol earlier, we uppercase this character
            if capitalize_next:
                char = char.upper()
                capitalize_next = False
            
            result.append(char)
         # Move to the next
        i += 6 

    return ''.join(result)  

def text_to_braille(text):
    result = []
    number_mode = False

    for char in text:
        if char.isdigit():
            if not number_mode:
                # a number and we're not in number mode -->  add the number symbol
                result.append(english_to_braille['Number'])
                number_mode = True
            # Convert the digit to its Braille equivalent
            result.append(english_to_braille[list(number_mapping.keys())[int(char)]])
        elif char.isalpha():
            if number_mode:
                # a letter after being in number mode --> add a space to exit number mode
                result.append(english_to_braille[' '])
                number_mode = False
            if char.isupper():
                # uppercase letters --> add the capital symbol before the letter
                result.append(english_to_braille['Capital'])
                result.append(english_to_braille[char.lower()])
            else:
                # lowercase letters
                result.append(english_to_braille[char.upper()])
        elif char == ' ':
            if number_mode:
                number_mode = False
            result.append(english_to_braille[' '])
        else:
            pass

    return ''.join(result) 

def main():
    if len(sys.argv) < 2:
        print("Yo, you gotta give me a string to translate!")
        return

    input_string = ' '.join(sys.argv[1:])

    # check out if the input is Braille or regular text
    if all(c in 'O.' for c in input_string) and len(input_string) % 6 == 0:
        # If it's all 'O' and '.' and its length is divisible by 6 --> Braille
        print(braille_to_text(input_string))
    else:
        # assume regular text
        print(text_to_braille(input_string))

if __name__ == "__main__":
    main()
