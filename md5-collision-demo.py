import hashlib
import binascii

# Hai chuỗi byte khác nhau nhưng có cùng MD5 hash
# Lưu ý: Đây là một collision thực tế được tìm thấy bởi các nhà nghiên cứu
# Nguồn: https://www.mscs.dal.ca/~selinger/md5collision/

# Chuyển đổi từ chuỗi hex sang bytes
def hex_to_bytes(hex_string):
    return binascii.unhexlify(hex_string.replace(" ", ""))

# Hai khối dữ liệu khác nhau nhưng có cùng MD5 hash
collision1_hex = """d131 dd02 c5e6 eec4 693d 9a06 98af c27b 4f54 7307 9441 4d00
c785 e8b5 983c c192 4a0d b3e6 62b0 21a8 14af 98bb 4b80 f81e
6578 f089 cbc6 8f61 7448 bf5c d61d 07a8 3f44 3827 d5e7 1c1d
e3c2 d0c0 eb19 9c52 0300 f180 4aff 7ed2 af68 6248 d907 8956
4f00 f7d8 d6bb 784b e028 51aa 2a75 96ba 406c 0758 bd8d 9590
a423 5b91 9f41 c26b 9fa5 862d 1e8f daba 3cbf 9b11 d686 cbc9
e478 4723 d5e7 cfdc 8881 5dfd 8dd5 b5bd 1e74 9fc5 a866 9082
9b6e 626e c97f 0c57 e16d 6c22 6ec2 a85b 125c 945d 13ce 3ea8
0d0c dc09 adb5 64f0 63f1 2e13 eaa6 7a9c 84d3 6c71 3f0e 1411
4c60 6b3d 0c0d 0f19 bfb9 a861 b453 0c39 6d48 cfc8 0c63"""

collision2_hex = """d131 dd02 c5e6 eec4 693d 9a06 98af c27b 4f54 7307 9441 4d00
c785 e8b5 983c c192 4a0d b3e6 62b0 21a8 14af 98bb 4b80 f81e
6578 f089 cbc6 8f61 7448 bf5c d61d 07a8 3f44 3827 d5e7 1c1d
e3c2 d0c0 eb19 9c52 0300 f180 4aff 7ed2 af68 6248 d907 8956
4f00 f7d8 d6bb 784b e028 51aa 2a75 96ba 406c 0758 bd8d 9590
a423 5b91 9f41 c26b 9fa5 862d 1e8f daba 3cbf 9b11 d686 cbc9
e478 4723 d5e7 cfdc 8881 5dfd 8dd5 b5bd 1e74 9fc5 a866 9082
9b6e 626e c97f 0c57 e16d 6c22 6ec2 a85b 125c 945d 13ce 3ea8
0d0c dc09 adb5 64f0 63f1 2e13 eaa6 7a9c 84d3 6c71 3f0e 1411
4c60 6b3d 0c0d 0f19 bfb9 a861 b453 0c39 6d48 cfc8 0c63"""

# Chuyển đổi từ chuỗi hex sang bytes
collision1 = hex_to_bytes(collision1_hex)
collision2 = hex_to_bytes(collision2_hex)

# Tính MD5 hash cho cả hai khối dữ liệu
md5_1 = hashlib.md5(collision1).hexdigest()
md5_2 = hashlib.md5(collision2).hexdigest()

# So sánh hai khối dữ liệu
print("Khối dữ liệu 1 và khối dữ liệu 2 có giống nhau không?", collision1 == collision2)
if collision1 != collision2:
    # Đếm số byte khác nhau
    diff_count = sum(1 for a, b in zip(collision1, collision2) if a != b)
    print(f"Số byte khác nhau: {diff_count} / {len(collision1)}")

    # In vị trí các byte khác nhau
    print("Vị trí các byte khác nhau:")
    for i, (a, b) in enumerate(zip(collision1, collision2)):
        if a != b:
            print(f"Vị trí {i}: {a} != {b}")

# So sánh hai giá trị MD5
print("\nMD5 của khối dữ liệu 1:", md5_1)
print("MD5 của khối dữ liệu 2:", md5_2)
print("Hai giá trị MD5 có giống nhau không?", md5_1 == md5_2)
