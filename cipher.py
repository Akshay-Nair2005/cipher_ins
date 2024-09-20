def create_mappings(key_value):
    from sympy import primerange
    
    # Divide the alphabet into sets based on the key value
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    sets = [alphabet[i:i + key_value] for i in range(0, len(alphabet), key_value)]
    
    # Get the required number of prime numbers
    prime_numbers = list(primerange(2, 2 + len(sets) * 10))[:len(sets)]
    
    # Print the sets and their corresponding prime numbers
    for set_num, letters in enumerate(sets):
        prime_num = prime_numbers[set_num]
        print(f"Set {set_num + 1} (Prime: {prime_num}): {letters}")
    
    # Create a dictionary to map each letter to its set and position
    letter_to_code = {}
    code_to_letter = {}
    for set_num, letters in enumerate(sets):
        prime_num = prime_numbers[set_num]
        for pos, letter in enumerate(letters, start=1):
            encrypted_value = prime_num ** pos
            letter_to_code[letter] = encrypted_value
            code_to_letter[encrypted_value] = letter
    
    return letter_to_code, code_to_letter

def encrypt_text(text, letter_to_code):
    encrypted_text = []
    print("\nEncryption Steps:")
    for char in text.upper().replace(" ", ""):
        if char in letter_to_code:
            encrypted_value = letter_to_code[char]
            binary_value = bin(encrypted_value)[2:].zfill(50)  # Pad to 50 digits
            encrypted_text.append(binary_value)
            print(f"{char} -> {encrypted_value} -> {binary_value}")
        else:
            # Handle non-alphabet characters
            binary_value = bin(ord(char))[2:].zfill(50)  # Pad to 50 digits
            encrypted_text.append(binary_value)
            print(f"{char} (non-alphabet) -> {ord(char)} -> {binary_value}")
    
    return ''.join(encrypted_text)

def decrypt_text(encrypted_text, code_to_letter):
    decrypted_text = []
    print("\nDecryption Steps:")
    for i in range(0, len(encrypted_text), 50):  # Process 50-digit binary chunks
        binary_value = encrypted_text[i:i+50]
        num_value = int(binary_value, 2)
        if num_value in code_to_letter:
            decrypted_text.append(code_to_letter[num_value])
            print(f"{binary_value} -> {num_value} -> {code_to_letter[num_value]}")
        else:
            # Handle non-alphabet characters
            decrypted_text.append(chr(num_value))
            print(f"{binary_value} (non-alphabet) -> {num_value} -> {chr(num_value)}")
    
    return ''.join(decrypted_text)

# Take key value from the user
key_value = int(input("Enter the key value (1 to 9) to determine the set size: "))

# Validate key value
if not 1 <= key_value <= 9:
    print("Invalid key value. Please enter a number between 1 and 9.")
else:
    # Create mappings
    letter_to_code, code_to_letter = create_mappings(key_value)

    # Take input from the user
    user_input = input("Enter the text to encrypt: ")

    # Encrypt the input text
    encrypted = encrypt_text(user_input, letter_to_code)
    print(f"\nEncrypted text: {encrypted}")

    # Decrypt the encrypted text
    decrypted = decrypt_text(encrypted, code_to_letter)
    print(f"\nDecrypted text: {decrypted}")
