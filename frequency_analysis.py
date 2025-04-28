import numpy as np
import matplotlib.pyplot as plt

# English letter frequencies (approximate)
ENGLISH_FREQUENCIES = {
    'A': 0.0817, 'B': 0.0149, 'C': 0.0278, 'D': 0.0425, 'E': 0.1270, 'F': 0.0223,
    'G': 0.0202, 'H': 0.0609, 'I': 0.0697, 'J': 0.0015, 'K': 0.0077, 'L': 0.0402,
    'M': 0.0241, 'N': 0.0675, 'O': 0.0751, 'P': 0.0193, 'Q': 0.0009, 'R': 0.0599,
    'S': 0.0633, 'T': 0.0906, 'U': 0.0276, 'V': 0.0098, 'W': 0.0236, 'X': 0.0015,
    'Y': 0.0197, 'Z': 0.0007
}

def calculate_frequencies(text):
    """
    Calculate the frequency of each letter in the text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: A dictionary with letter frequencies
    """
    # Count occurrences of each letter
    letter_counts = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        letter_counts[letter] = 0
    
    # Count letters in the text
    text = text.upper()
    for char in text:
        if char in letter_counts:
            letter_counts[char] += 1
    
    # Convert counts to frequencies
    total_letters = sum(letter_counts.values())
    frequencies = {}
    
    if total_letters > 0:
        for letter, count in letter_counts.items():
            frequencies[letter] = count / total_letters
    else:
        frequencies = {letter: 0 for letter in letter_counts}
    
    return frequencies

def plot_frequencies(frequencies, title="Letter Frequencies"):
    """
    Plot letter frequencies.
    
    Args:
        frequencies (dict): Dictionary with letter frequencies
        title (str): Title for the plot
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    letters = list(frequencies.keys())
    freqs = list(frequencies.values())
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(letters, freqs, color='skyblue')
    ax.set_xlabel('Letter')
    ax.set_ylabel('Frequency')
    ax.set_title(title)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add line for English frequencies for comparison
    if all(letter in ENGLISH_FREQUENCIES for letter in letters):
        english_freqs = [ENGLISH_FREQUENCIES[letter] for letter in letters]
        ax.plot(letters, english_freqs, 'ro-', alpha=0.7, label='English average')
        ax.legend()
    
    return fig

def calculate_index_of_coincidence(text):
    """
    Calculate the index of coincidence for a text.
    
    The index of coincidence is the probability that two randomly selected
    letters in the text are the same.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        float: The index of coincidence
    """
    # Count occurrences of each letter
    letter_counts = {}
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        letter_counts[letter] = 0
    
    # Count letters in the text
    text = text.upper()
    for char in text:
        if char in letter_counts:
            letter_counts[char] += 1
    
    # Calculate the index of coincidence
    n = sum(letter_counts.values())
    
    if n <= 1:  # Not enough text to calculate IoC
        return 0
    
    sum_frequencies = sum(count * (count - 1) for count in letter_counts.values())
    ic = sum_frequencies / (n * (n - 1))
    
    return ic

def analyze_vigenere_key_length(ciphertext, max_length=20):
    """
    Analyze a Vigenère ciphertext to find the most likely key length
    using the index of coincidence.
    
    Args:
        ciphertext (str): The ciphertext to analyze
        max_length (int): Maximum key length to consider
        
    Returns:
        dict: A dictionary with key lengths and their IoC scores
    """
    # Normalize input
    ciphertext = ''.join(c.upper() for c in ciphertext if c.isalpha())
    
    # Limit max_length to the length of the ciphertext
    max_length = min(max_length, len(ciphertext) // 2)
    
    results = {}
    
    # Try different key lengths
    for key_length in range(1, max_length + 1):
        # Split the ciphertext into 'key_length' groups
        groups = [''] * key_length
        
        for i, char in enumerate(ciphertext):
            groups[i % key_length] += char
        
        # Calculate the average IoC for all groups
        total_ic = 0
        for group in groups:
            total_ic += calculate_index_of_coincidence(group)
        
        avg_ic = total_ic / key_length
        results[key_length] = avg_ic
    
    return results

def break_vigenere_cipher(ciphertext, key_length):
    """
    Attempt to break a Vigenère cipher when the key length is known.
    
    Args:
        ciphertext (str): The ciphertext to break
        key_length (int): The length of the key
        
    Returns:
        tuple: (decrypted_text, discovered_key)
    """
    # Normalize input
    ciphertext = ''.join(c.upper() for c in ciphertext if c.isalpha())
    
    # Split the ciphertext into key_length groups
    groups = [''] * key_length
    for i, char in enumerate(ciphertext):
        groups[i % key_length] += char
    
    discovered_key = ""
    
    # For each group, find the shift that gives frequencies closest to English
    for group in groups:
        best_shift = 0
        best_score = float('inf')
        
        # Try each possible shift
        for shift in range(26):
            # Decrypt with this shift
            decrypted = ''.join(chr(((ord(c) - ord('A') - shift) % 26) + ord('A')) for c in group)
            
            # Calculate frequency distribution
            freqs = calculate_frequencies(decrypted)
            
            # Calculate chi-squared statistic (measure of how well frequencies match English)
            chi_squared = sum(
                ((freqs.get(letter, 0) - ENGLISH_FREQUENCIES[letter]) ** 2) / ENGLISH_FREQUENCIES[letter]
                for letter in ENGLISH_FREQUENCIES
            )
            
            # Update best shift if this is better
            if chi_squared < best_score:
                best_score = chi_squared
                best_shift = shift
        
        # Add the best shift to the key (as a letter)
        discovered_key += chr(best_shift + ord('A'))
    
    # Decrypt the whole ciphertext with the discovered key
    from vigenere_cipher import decrypt_vigenere
    decrypted_text = decrypt_vigenere(ciphertext, discovered_key)
    
    return decrypted_text, discovered_key
