from sympy import primerange
from collections import Counter
import string

def create_mappings(key_value):
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
            binary_value = bin(encrypted_value)[2:].zfill(31)
            encrypted_text.append(binary_value)
            print(f"{char} -> {encrypted_value} -> {binary_value}")
        else:
            # Handle non-alphabet characters
            binary_value = bin(ord(char))[2:].zfill(31)
            encrypted_text.append(binary_value)
            print(f"{char} (non-alphabet) -> {ord(char)} -> {binary_value}")
    
    return ''.join(encrypted_text)

def decrypt_text(encrypted_text, code_to_letter):
    decrypted_text = []
    print("\nDecryption Steps:")
    for i in range(0, len(encrypted_text), 31):
        binary_value = encrypted_text[i:i+31]
        num_value = int(binary_value, 2)
        if num_value in code_to_letter:
            decrypted_text.append(code_to_letter[num_value])
            print(f"{binary_value} -> {num_value} -> {code_to_letter[num_value]}")
        else:
            # Handle non-alphabet characters
            decrypted_text.append(chr(num_value))
            print(f"{binary_value} (non-alphabet) -> {num_value} -> {chr(num_value)}")
    
    return ''.join(decrypted_text)

def frequency_analysis(encrypted_text):
    segment_length = 31  # Each character is encoded into a 31-bit binary string
    segments = [encrypted_text[i:i+segment_length] for i in range(0, len(encrypted_text), segment_length)]
    frequency_counter = Counter(segments)
    
    # Print the frequency analysis results
    print("\nFrequency Analysis of Encrypted Text:")
    for segment, count in frequency_counter.most_common():
        print(f"Binary Segment: {segment}, Count: {count}")
    
    return frequency_counter

def get_english_letter_frequencies():
    english_freq = {
        'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
        'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
        'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
        'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
        'U': 2.758, 'V': 0.978, 'W': 2.361, 'X': 0.150, 'Y': 1.974,
        'Z': 0.074
    }
    total = sum(english_freq.values())
    for letter in english_freq:
        english_freq[letter] = english_freq[letter] / total * 100
    
    return english_freq

def analyze_encrypted_text(frequency_counter, code_to_letter, english_freq):
    # Attempt to match the most frequent encrypted segments with the most frequent English letters
    most_common_segments = [segment for segment, count in frequency_counter.most_common()]
    sorted_english_freq = sorted(english_freq.items(), key=lambda x: -x[1])
    most_common_letters = [letter for letter, freq in sorted_english_freq]
    
    possible_mappings = {}
    print("\nAttempting to Map Frequent Encrypted Segments to English Letters:")
    for i in range(min(len(most_common_segments), len(most_common_letters))):
        segment = most_common_segments[i]
        letter = most_common_letters[i]
        num_value = int(segment, 2)
        if num_value in code_to_letter:
            possible_mappings[segment] = letter
            print(f"Binary Segment: {segment} (Value: {num_value}) -> Possible Letter: {letter}")
        else:
            print(f"Binary Segment: {segment} (Value: {num_value}) -> No direct mapping found")

    return possible_mappings

# Take key value from the user
key_value = int(input("Enter the key value (1 to 9) to determine the set size: "))

# Validate key value
if not 1 <= key_value <= 9:
    print("Invalid key value. Please enter a number between 1 and 9.")
else:
    # Create mappings
    letter_to_code, code_to_letter = create_mappings(key_value)

    # Sample text for encryption
    sample_text = "Group"

    # Encrypt the sample text
    encrypted_sample = encrypt_text(sample_text, letter_to_code)
    print(f"\nEncrypted text: {encrypted_sample}")

    # Decrypt the encrypted text
    decrypted = decrypt_text(encrypted_sample, code_to_letter)
    print(f"\nDecrypted text: {decrypted}")

    # Perform frequency analysis on the encrypted sample text
    frequency_counter = frequency_analysis(encrypted_sample)

    # Get expected English letter frequencies
    english_freq = get_english_letter_frequencies()

    # Print expected English letter frequencies
    print("\nExpected English Letter Frequencies:")
    for letter, freq in sorted(english_freq.items(), key=lambda x: -x[1]):
        print(f"Letter: {letter}, Frequency: {freq:.2f}%")

    # Analyze the encrypted text
    possible_mappings = analyze_encrypted_text(frequency_counter, code_to_letter, english_freq)

    print("\nPossible Mappings from Frequency Analysis:")
    for segment, letter in possible_mappings.items():
        print(f"Segment: {segment} -> Letter: {letter}")
