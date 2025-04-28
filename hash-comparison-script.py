import hashlib

def calculate_hashes(text):
    """Tính giá trị băm SHA-256, SHA-3 và MD5 cho văn bản đầu vào."""
    # Chuyển đổi văn bản thành bytes
    text_bytes = text.encode('utf-8')
    
    # Tính SHA-256
    sha256_hash = hashlib.sha256(text_bytes).hexdigest()
    
    # Tính SHA-3 (SHA3-256)
    sha3_hash = hashlib.sha3_256(text_bytes).hexdigest()
    
    # Tính MD5
    md5_hash = hashlib.md5(text_bytes).hexdigest()
    
    return {
        'SHA-256': sha256_hash,
        'SHA-3': sha3_hash,
        'MD5': md5_hash
    }

def compare_hashes(text1, text2):
    """So sánh giá trị băm của hai văn bản."""
    hashes1 = calculate_hashes(text1)
    hashes2 = calculate_hashes(text2)
    
    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print("\nSo sánh hash values:")
    print("-" * 70)
    
    for hash_type in hashes1:
        hash1 = hashes1[hash_type]
        hash2 = hashes2[hash_type]
        print(f"{hash_type}:")
        print(f"Text 1: {hash1}")
        print(f"Text 2: {hash2}")
        # Tính số bit khác nhau
        binary1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
        binary2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
        diff_bits = sum(b1 != b2 for b1, b2 in zip(binary1, binary2))
        total_bits = len(binary1)
        diff_percentage = (diff_bits / total_bits) * 100
        print(f"Số bit khác nhau: {diff_bits}/{total_bits} ({diff_percentage:.2f}%)")
        print("-" * 70)

# Thử nghiệm với hai văn bản chỉ khác nhau một ký tự
text1 = "Đây là một văn bản mẫu để kiểm tra tính chất của hàm băm."
text2 = "Đây là một văn bản mẫu để kiểm tra tính chất của hàm băm!"  # Thêm dấu chấm than

compare_hashes(text1, text2)

# Lưu kết quả ra file
def save_hashes_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        hashes = calculate_hashes(text)
        for hash_type, hash_value in hashes.items():
            f.write(f"{hash_type}: {hash_value}\n")

save_hashes_to_file("hash_results_original.txt", text1)
save_hashes_to_file("hash_results_modified.txt", text2)

print("\nĐã lưu kết quả vào files hash_results_original.txt và hash_results_modified.txt")
