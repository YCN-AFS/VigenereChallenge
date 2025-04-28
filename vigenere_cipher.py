def caesar_shift(char, shift):
    """
    Shifts a single character by the specified amount (Caesar cipher).
    
    Args:
        char (str): A single uppercase letter
        shift (int): The amount to shift the letter by
        
    Returns:
        str: The shifted character
    """
    if not char.isalpha():
        return char
        
    # Convert to 0-25 range
    char_code = ord(char.upper()) - ord('A')
    
    # Apply shift and wrap around with modulo
    shifted_code = (char_code + shift) % 26
    
    # Convert back to character
    return chr(shifted_code + ord('A'))

def encrypt_vigenere(plaintext, key):
    """
    Encrypt plaintext using the Vigenère cipher with the given key.
    
    Args:
        plaintext (str): The text to encrypt (uppercase letters only)
        key (str): The encryption key (uppercase letters only)
        
    Returns:
        str: The encrypted ciphertext
    """
    # Normalize inputs - convert to uppercase and remove non-alphabetic characters
    plaintext = ''.join(c.upper() for c in plaintext if c.isalpha())
    key = ''.join(c.upper() for c in key if c.isalpha())
    
    if not key:
        raise ValueError("Key must contain at least one alphabetic character")
    
    result = ""
    
    for i in range(len(plaintext)):
        # Get the current key character (cycling through the key)
        key_char = key[i % len(key)]
        
        # Convert key character to shift value (A=0, B=1, ..., Z=25)
        shift = ord(key_char) - ord('A')
        
        # Shift the plaintext character and add to result
        result += caesar_shift(plaintext[i], shift)
    
    return result

def decrypt_vigenere(ciphertext, key):
    """
    Decrypt ciphertext using the Vigenère cipher with the given key.
    
    Args:
        ciphertext (str): The text to decrypt (uppercase letters only)
        key (str): The decryption key (uppercase letters only)
        
    Returns:
        str: The decrypted plaintext
    """
    # Normalize inputs - convert to uppercase and remove non-alphabetic characters
    ciphertext = ''.join(c.upper() for c in ciphertext if c.isalpha())
    key = ''.join(c.upper() for c in key if c.isalpha())
    
    if not key:
        raise ValueError("Key must contain at least one alphabetic character")
    
    result = ""
    
    for i in range(len(ciphertext)):
        # Get the current key character (cycling through the key)
        key_char = key[i % len(key)]
        
        # Convert key character to shift value (A=0, B=1, ..., Z=25)
        shift = ord(key_char) - ord('A')
        
        # For decryption, shift in the opposite direction
        # This is equivalent to shifting by (26 - shift) % 26
        result += caesar_shift(ciphertext[i], (26 - shift) % 26)
    
    return result
