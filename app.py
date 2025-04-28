import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from vigenere_cipher import encrypt_vigenere, decrypt_vigenere, caesar_shift
from frequency_analysis import (
    calculate_frequencies, 
    plot_frequencies, 
    analyze_vigenere_key_length,
    break_vigenere_cipher
)
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import random
import os

# Setup translations
translator = Translator()

def translate_text(text, dest='vi'):
    """Translate text to the target language"""
    try:
        translation = translator.translate(text, dest=dest)
        return translation.text
    except Exception as e:
        # Fall back to original text if translation fails
        st.error(f"Translation error: {e}")
        return text

# App configuration
st.set_page_config(
    page_title="Thử Thách Mật Mã Vigenère",  # Vigenère Cipher Challenge
    page_icon="🔐",
    layout="wide"
)

# Vietnamese Translation dictionaries
translations = {
    "title": "🔐 Thử Thách Mật Mã Vigenère",
    "introduction": """
    ## Giới thiệu
    
    Mật mã Vigenère là một phương pháp mã hóa văn bản bảng chữ cái bằng cách sử dụng một dạng thay thế đa bảng chữ cái đơn giản.
    Nó được coi là không thể phá vỡ trong hơn 300 năm!
    
    Khác với mật mã Caesar chỉ sử dụng một giá trị dịch chuyển duy nhất, mật mã Vigenère sử dụng một **từ khóa** để xác định
    các giá trị dịch chuyển khác nhau cho các vị trí khác nhau trong văn bản, làm cho nó an toàn hơn nhiều.
    
    Trong phòng thí nghiệm này, bạn sẽ:
    1. Học cách mật mã Vigenère hoạt động
    2. Thực hiện các thuật toán mã hóa và giải mã
    3. Thử phá vỡ mật mã bằng phân tích tần suất
    4. So sánh bảo mật của mật mã Vigenère và Caesar
    
    Hãy bắt đầu cuộc phiêu lưu mật mã của bạn!
    """,
    "level": "Cấp độ",
    "mission": "Nhiệm vụ",
    "complete": "Hoàn thành",
    "encrypt": "Mã hóa",
    "decrypt": "Giải mã",
    "challenge": "Thử thách",
    "next_level": "Cấp độ tiếp theo",
    "congrats": "Chúc mừng!",
    "try_again": "Hãy thử lại",
    "mission_complete": "Nhiệm vụ hoàn thành!",
    "correct": "Chính xác!",
    "incorrect": "Không chính xác!",
}

def generate_badge(text, color="#4CAF50"):
    """Generate a colorful badge image with text"""
    width, height = 300, 100
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default if not available
    try:
        font = ImageFont.truetype("Arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    # Center text
    try:
        # For newer Pillow versions
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        # For older Pillow versions
        text_width, text_height = draw.textsize(text, font=font)
    
    position = ((width-text_width)//2, (height-text_height)//2)
    
    # Draw text with a slight shadow for 3D effect
    draw.text((position[0]+2, position[1]+2), text, font=font, fill="#000000")
    draw.text(position, text, font=font, fill="#FFFFFF")
    
    # Convert to base64 for embedding in page
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Initialize session state
if 'game_level' not in st.session_state:
    st.session_state.game_level = 1
if 'challenges_completed' not in st.session_state:
    st.session_state.challenges_completed = 0
if 'show_animation' not in st.session_state:
    st.session_state.show_animation = False
if 'mission_completed' not in st.session_state:
    st.session_state.mission_completed = False
if 'ui_language' not in st.session_state:
    st.session_state.ui_language = 'vi'  # Default to Vietnamese
if 'level1_answer' not in st.session_state:
    st.session_state.level1_answer = ""
if 'level1_submitted' not in st.session_state:
    st.session_state.level1_submitted = False
if 'level1_correct' not in st.session_state:
    st.session_state.level1_correct = False
if 'level2_key' not in st.session_state:
    st.session_state.level2_key = ""
if 'level2_answer' not in st.session_state:
    st.session_state.level2_answer = ""
if 'level2_submitted' not in st.session_state:
    st.session_state.level2_submitted = False
if 'level2_correct' not in st.session_state:
    st.session_state.level2_correct = False
if 'level3_submitted' not in st.session_state:
    st.session_state.level3_submitted = False
if 'level3_correct' not in st.session_state:
    st.session_state.level3_correct = False
if 'final_challenge_completed' not in st.session_state:
    st.session_state.final_challenge_completed = False

def complete_challenge():
    st.session_state.challenges_completed += 1
    st.session_state.show_animation = True
    if st.session_state.challenges_completed >= 3:
        st.session_state.mission_completed = True

def level_up(level=None):
    if level:
        st.session_state.game_level = level
    else:
        st.session_state.game_level += 1
    st.session_state.show_animation = True
    
def update_level1_answer():
    st.session_state.level1_submitted = True
    correct_answer = encrypt_vigenere("VIETNAM", "KEY")
    if st.session_state.level1_answer.upper() == correct_answer:
        st.session_state.level1_correct = True
        complete_challenge()

def update_level2_answer():
    st.session_state.level2_submitted = True
    if st.session_state.level2_key.upper() == "HANOI" and st.session_state.level2_answer.upper() == "CHUCMUNGBANDALAMNENLEVEL":
        st.session_state.level2_correct = True
        complete_challenge()

def update_level3_answer(selected_option):
    st.session_state.level3_submitted = True
    if selected_option == "Hướng dẫn về bảo mật thông tin":
        st.session_state.level3_correct = True
        complete_challenge()

def show_encryption_steps(plaintext, key, ciphertext):
    # Create a table showing the encryption process
    data = []
    extended_key = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]
    
    for i in range(len(plaintext)):
        p_char = plaintext[i]
        k_char = extended_key[i]
        c_char = ciphertext[i]
        
        p_num = ord(p_char) - ord('A')
        k_num = ord(k_char) - ord('A')
        c_num = (p_num + k_num) % 26
        
        data.append([
            i+1,
            p_char,
            p_num,
            k_char,
            k_num,
            f"({p_num} + {k_num}) % 26 = {c_num}",
            c_char
        ])
    
    # Display as a table
    table = "| Bước | Văn bản gốc | P (0-25) | Khóa | K (0-25) | Tính toán | Mật mã |\n"
    table += "|------|-----------|----------|-----|----------|-------------|------------|\n"
    
    for row in data:
        table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |\n"
    
    st.markdown(table)

def show_decryption_steps(ciphertext, key, plaintext):
    # Create a table showing the decryption process
    data = []
    extended_key = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]
    
    for i in range(len(ciphertext)):
        c_char = ciphertext[i]
        k_char = extended_key[i]
        p_char = plaintext[i]
        
        c_num = ord(c_char) - ord('A')
        k_num = ord(k_char) - ord('A')
        p_num = (c_num - k_num) % 26
        
        data.append([
            i+1,
            c_char,
            c_num,
            k_char,
            k_num,
            f"({c_num} - {k_num}) % 26 = {p_num}",
            p_char
        ])
    
    # Display as a table
    table = "| Bước | Mật mã | C (0-25) | Khóa | K (0-25) | Tính toán | Văn bản gốc |\n"
    table += "|------|------------|----------|-----|----------|-------------|----------|\n"
    
    for row in data:
        table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |\n"
    
    st.markdown(table)

def level_1_intro():
    st.markdown(translations["introduction"])
    
    st.markdown("## Nguyên tắc cơ bản của Mật mã Vigenère")
    
    st.markdown("""
    Mật mã Vigenère sử dụng một **từ khóa** lặp lại để tạo ra một dòng khóa. Mỗi chữ cái trong từ khóa
    xác định mức độ dịch chuyển của mỗi chữ cái tương ứng trong văn bản gốc.
    
    Ví dụ, nếu từ khóa của bạn là "KEY":
    - Chữ cái thứ 1 của văn bản gốc được dịch chuyển bởi K (tức là 10 vị trí)
    - Chữ cái thứ 2 được dịch chuyển bởi E (4 vị trí)
    - Chữ cái thứ 3 được dịch chuyển bởi Y (24 vị trí)
    - Chữ cái thứ 4 được dịch chuyển bởi K một lần nữa, vì từ khóa lặp lại
    
    Đây là một **mật mã thay thế đa bảng chữ cái**, có nghĩa là nó sử dụng nhiều bảng chữ cái thay thế.
    """)
    
    # Visualization of how the cipher works
    st.subheader("Bảng Vigenère (Tabula Recta)")
    
    # Creating the Vigenère square using a monospaced font in markdown
    square = "```\n   " + " ".join([chr(65+i) for i in range(26)]) + "\n"
    square += "  +" + "-" * 51 + "\n"
    
    for i in range(26):
        row = chr(65+i) + " | "
        for j in range(26):
            # Calculate the letter for this position in the Vigenère square
            letter = chr(65 + (i + j) % 26)
            row += letter + " "
        square += row + "\n"
    
    square += "```"
    
    st.markdown(square)
    
    st.markdown("""
    ### Cách sử dụng Bảng Vigenère:
    
    1. Tìm hàng bắt đầu bằng chữ cái khóa
    2. Tìm cột được đánh đầu bởi chữ cái văn bản gốc
    3. Chữ cái tại giao điểm là chữ cái mật mã
    
    ### Ví dụ
    
    - Văn bản gốc: `HELLO`
    - Khóa: `KEY` (lặp lại thành `KEYKE`)
    
    | Văn bản gốc | Khóa | Dịch chuyển | Mật mã |
    |-------------|------|-------------|--------|
    | H           | K    | 10          | R      |
    | E           | E    | 4           | I      |
    | L           | Y    | 24          | J      |
    | L           | K    | 10          | V      |
    | O           | E    | 4           | S      |
    
    Vậy "HELLO" được mã hóa với khóa "KEY" trở thành "RIJVS"
    """)
    
    st.info("💡 Công thức toán học cho mã hóa Vigenère là: C = (P + K) % 26, trong đó C là mật mã, P là văn bản gốc, và K là chữ cái khóa (tất cả được chuyển đổi thành số từ 0-25)")
    
    # Quiz to move to next level
    st.markdown("### 🎮 Thử thách để mở khóa Cấp độ 2")
    
    st.text_input("Mã hóa từ 'VIETNAM' với khóa 'KEY'. Nhập kết quả của bạn:", 
                 key="level1_answer", on_change=update_level1_answer)
    
    if st.session_state.level1_submitted:
        if st.session_state.level1_correct:
            st.success(f"{translations['correct']} '{encrypt_vigenere('VIETNAM', 'KEY')}' là câu trả lời đúng!")
            st.balloons()
            
            # Show next level button
            if st.button(f"{translations['next_level']} ➡️", key="level1_next"):
                level_up(2)
        else:
            st.error(f"{translations['incorrect']} Hãy thử lại!")

def level_2_encryption_decryption():
    st.header("Cấp độ 2: Mã hóa & Giải mã")
    
    st.markdown("""
    Chào mừng bạn đến với Cấp độ 2! Bây giờ bạn sẽ học cách mã hóa và giải mã thông điệp bằng mật mã Vigenère.
    
    Hãy thử mã hóa và giải mã một số thông điệp để hiểu rõ hơn cách thức hoạt động.
    """)
    
    tab1, tab2 = st.tabs(["🔒 Mã hóa", "🔓 Giải mã"])
    
    with tab1:
        st.subheader("Mã hóa thông điệp")
        plaintext = st.text_area("Nhập văn bản gốc để mã hóa:", "XINCHAO", key="encrypt_plaintext")
        key = st.text_input("Nhập khóa mã hóa:", "KEY", key="encrypt_key")
        
        if st.button("Mã hóa", key="encrypt_button"):
            if not key or not plaintext:
                st.error("Vui lòng nhập cả văn bản gốc và khóa")
            else:
                # Process inputs
                plaintext = ''.join(c.upper() for c in plaintext if c.isalpha())
                key = ''.join(c.upper() for c in key if c.isalpha())
                
                if not key or not plaintext:
                    st.error("Vui lòng nhập văn bản chữ cái hợp lệ cho văn bản gốc và khóa")
                else:
                    ciphertext = encrypt_vigenere(plaintext, key)
                    st.success(f"Văn bản mã hóa: **{ciphertext}**")
                    
                    # Show the encryption process
                    st.markdown("### Quá trình mã hóa:")
                    show_encryption_steps(plaintext, key, ciphertext)
    
    with tab2:
        st.subheader("Giải mã thông điệp")
        ciphertext = st.text_area("Nhập mật mã để giải mã:", "BOJRZU", key="decrypt_ciphertext")
        key = st.text_input("Nhập khóa giải mã:", "KEY", key="decrypt_key")
        
        if st.button("Giải mã", key="decrypt_button"):
            if not key or not ciphertext:
                st.error("Vui lòng nhập cả mật mã và khóa")
            else:
                # Process inputs
                ciphertext = ''.join(c.upper() for c in ciphertext if c.isalpha())
                key = ''.join(c.upper() for c in key if c.isalpha())
                
                if not key or not ciphertext:
                    st.error("Vui lòng nhập văn bản chữ cái hợp lệ cho mật mã và khóa")
                else:
                    plaintext = decrypt_vigenere(ciphertext, key)
                    st.success(f"Văn bản giải mã: **{plaintext}**")
                    
                    # Show the decryption process
                    st.markdown("### Quá trình giải mã:")
                    show_decryption_steps(ciphertext, key, plaintext)
    
    # Challenge to move to the next level
    st.markdown("---")
    st.markdown("### 🎮 Thử thách Giải mã")
    
    st.markdown("""
    Để mở khóa Cấp độ 3, bạn cần giải mã thông điệp bí mật này:
    
    Mật mã: **FRBCFNOFMMYBKCVLISIXMEH**
    
    Gợi ý: Khóa mã hóa là tên một thành phố lớn ở Việt Nam (viết liền không dấu).
    """)
    
    # Input fields for the challenge
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nhập khóa bạn nghĩ là đúng:", key="level2_key")
    with col2:
        st.text_input("Nhập thông điệp đã giải mã:", key="level2_answer")
    
    # Button to check the answer
    if st.button("Kiểm tra câu trả lời", key="check_level2"):
        update_level2_answer()
    
    # Display results after submission
    if st.session_state.level2_submitted:
        if st.session_state.level2_correct:
            st.success(f"{translations['correct']} Bạn đã giải mã thành công thông điệp!")
            st.balloons()
            
            # Show next level button
            if st.button(f"{translations['next_level']} ➡️", key="level2_next"):
                level_up(3)
        else:
            if st.session_state.level2_key.upper() == "HANOI":
                st.warning("Khóa đúng! Nhưng thông điệp giải mã không chính xác. Hãy thử lại.")
            else:
                st.error(f"{translations['incorrect']} Hãy thử lại với một khóa khác.")

def level_3_breaking_cipher():
    st.header("Cấp độ 3: Phá Vỡ Mật Mã")
    
    st.markdown("""
    Chào mừng bạn đến với Cấp độ 3! Bây giờ chúng ta sẽ học cách phân tích và phá vỡ mật mã Vigenère.
    
    ### Phân tích tần suất
    
    Phá vỡ mật mã Vigenère phức tạp hơn so với mật mã Caesar, nhưng vẫn có thể thực hiện được bằng kỹ thuật phân tích tần suất:
    
    1. **Xác định độ dài khóa** - sử dụng phương pháp như kiểm tra Kasiski hoặc Chỉ số trùng khớp (Index of Coincidence)
    2. **Chia mật mã** thành các nhóm dựa trên độ dài khóa
    3. **Áp dụng phân tích tần suất** cho từng nhóm riêng lẻ (vì mỗi nhóm được mã hóa với cùng một độ dịch chuyển)
    4. **Kết hợp các kết quả** để khôi phục khóa
    """)
    
    st.subheader("So sánh mật mã Caesar và Vigenère")
    
    st.markdown("""
    ### Mật mã Caesar
    
    Mật mã Caesar là một mật mã thay thế đơn giản trong đó mỗi chữ cái trong văn bản gốc được dịch chuyển một số vị trí cố định.
    
    **Ưu điểm:**
    - Dễ thực hiện và sử dụng
    - Mã hóa và giải mã nhanh chóng với khóa
    
    **Nhược điểm:**
    - Chỉ có 25 khóa có thể (cho bảng chữ cái tiếng Anh)
    - Có thể bị phá vỡ bằng cách thử tất cả các khóa một cách nhanh chóng
    - Dễ bị tấn công phân tích tần suất (tần suất chữ cái vẫn giữ nguyên)
    
    ### Mật mã Vigenère
    
    Mật mã Vigenère sử dụng một từ khóa để xác định các giá trị dịch chuyển khác nhau cho các vị trí khác nhau trong văn bản.
    
    **Ưu điểm:**
    - Không gian khóa lớn hơn nhiều (26^k khả năng cho khóa có độ dài k)
    - Khả năng chống lại phân tích tần suất đơn giản
    - Nhiều chữ cái trong văn bản gốc có thể được mã hóa thành các chữ cái mật mã khác nhau
    
    **Nhược điểm:**
    - Vẫn dễ bị tấn công bởi các kỹ thuật phân tích mật mã nâng cao
    - Sự lặp lại của khóa tạo ra các mẫu có thể bị khai thác
    - Khi độ dài khóa được xác định, nó giảm xuống thành nhiều mật mã Caesar
    """)
    
    # Interactive demonstration
    st.subheader("Thử phá vỡ mật mã")
    
    st.markdown("""
    Bây giờ hãy thử phá vỡ một mật mã Vigenère khi biết độ dài khóa.
    
    Đây là một mật mã đã bị chặn từ một nguồn bí mật:
    
    **LWSSUCMZXMGZTTZSUOAXZWBHGWOMHXQVTVPVGAGZHTVTVVSMKFMTVIKHRZTWWWPMLZLGMXEOAGZJGMSMHMVCSWTXQVTVPBKHRZXWIIMATRVMPLRPV**
    
    Hãy sử dụng công cụ phân tích để tìm độ dài khóa!
    """)
    
    # Example ciphertext
    example_cipher = "LWSSUCMZXMGZTTZSUOAXZWBHGWOMHXQVTVPVGAGZHTVTVVSMKFMTVIKHRZTWWWPMLZLGMXEOAGZJGMSMHMVCSWTXQVTVPBKHRZXWIIMATRVMPLRPV"
    
    # Show IoC for different key lengths for the example
    key_length_data = analyze_vigenere_key_length(example_cipher, max_length=15)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    key_lengths = list(key_length_data.keys())
    index_values = list(key_length_data.values())
    
    ax.bar(key_lengths, index_values, color='skyblue')
    ax.set_xlabel('Độ dài khóa (Key Length)')
    ax.set_ylabel('Chỉ số trùng khớp (Index of Coincidence)')
    ax.set_title('Chỉ số trùng khớp cho các độ dài khóa khác nhau')
    ax.set_xticks(key_lengths)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.axhline(y=0.067, color='r', linestyle='-', alpha=0.7, label='Dự kiến cho tiếng Anh (Expected for English)')
    ax.legend()
    
    st.pyplot(fig)
    
    st.markdown("""
    Chỉ số trùng khớp (Index of Coincidence - IoC) đo xác suất hai chữ cái được chọn ngẫu nhiên trong một văn bản là giống nhau.
    
    - Đối với văn bản ngẫu nhiên, IoC ≈ 0.038
    - Đối với văn bản tiếng Anh, IoC ≈ 0.067
    
    Khi chúng ta chia mật mã thành các nhóm dựa trên độ dài khóa đúng, mỗi nhóm sẽ có IoC gần với văn bản tiếng Anh bình thường.
    
    **Dựa vào biểu đồ trên, độ dài khóa có thể là bao nhiêu?**
    """)
    
    user_key_length = st.number_input("Nhập độ dài khóa bạn cho là đúng:", min_value=1, max_value=15, value=5)
    
    if st.button("Thử phá mã", key="break_cipher_btn"):
        if user_key_length == 5:
            decrypted_text, discovered_key = break_vigenere_cipher(example_cipher, user_key_length)
            st.success(f"Độ dài khóa đúng! Khóa có thể là: {discovered_key}")
            st.markdown(f"Văn bản giải mã: **{decrypted_text}**")
            
            # Challenge to complete level 3
            st.markdown("### 🎮 Thử thách Phá mã")
            st.markdown("""
            Bây giờ hãy trả lời câu hỏi này dựa trên văn bản đã giải mã:
            
            Ý nghĩa của thông điệp là gì? (Chọn một trong các lựa chọn sau)
            """)
            
            message_meaning = st.radio(
                "Ý nghĩa của thông điệp:",
                ["Một bài thơ về tình yêu", "Một trích đoạn từ sách", "Hướng dẫn về bảo mật thông tin", "Kế hoạch bí mật"],
                key="level3_message_type"
            )
            
            # Button to submit the answer
            if st.button("Gửi câu trả lời", key="submit_level3"):
                update_level3_answer(message_meaning)
            
            # Display result after submission  
            if st.session_state.level3_submitted:
                if st.session_state.level3_correct:
                    st.success("Chính xác! Thông điệp là về bảo mật thông tin.")
                    st.balloons()
                    
                    # Show next level button
                    if st.button(f"{translations['next_level']} ➡️", key="level3_next"):
                        level_up(4)
                else:
                    st.error("Không chính xác. Hãy đọc kỹ thông điệp và thử lại!")
        else:
            st.error("Độ dài khóa không chính xác. Hãy xem kỹ biểu đồ và thử lại!")

def level_4_hacker_challenge():
    st.header("Cấp độ 4: Thử thách Hacker")
    
    st.markdown("""
    ## 🎖️ Thử thách cuối cùng
    
    Chúc mừng vì đã đến được thử thách cuối cùng! Bạn đã chứng minh được kỹ năng mật mã của mình.
    
    Trong thử thách này, bạn sẽ phải phá vỡ một mật mã Vigenère mà không biết khóa. 
    Bạn sẽ cần sử dụng tất cả kiến thức đã học về phân tích tần suất và các kỹ thuật phá mã.
    
    Đây là thông điệp bí mật cuối cùng:
    
    **PZSVYMFCCKIQXSZWRLFWOZGIILSWVMBZPESJLVYYVHWPIKBCMBGPLYPCDZMFOWVSLRLLRYCAZCKIQXSZRDAFDRVHZBQHYYVHWPIUBCWVDRLQMLVDEBVVBDTZWRLVVBDSEXZIGOEHQTVLWIMYWMDIFGGEIGGZRFBBX**
    
    Sứ mệnh của bạn:
    1. Xác định độ dài khóa bằng phân tích chỉ số trùng khớp (IoC)
    2. Tìm khóa
    3. Giải mã thông điệp
    
    Bạn có thể sử dụng các công cụ phân tích bên dưới để giúp bạn!
    """)
    
    # Final challenge ciphertext 
    final_cipher = "PZSVYMFCCKIQXSZWRLFWOZGIILSWVMBZPESJLVYYVHWPIKBCMBGPLYPCDZMFOWVSLRLLRYCAZCKIQXSZRDAFDRVHZBQHYYVHWPIUBCWVDRLQMLVDEBVVBDTZWRLVVBDSEXZIGOEHQTVLWIMYWMDIFGGEIGGZRFBBX"
    
    # Show IoC analysis for final challenge
    final_key_length_data = analyze_vigenere_key_length(final_cipher, max_length=15)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    key_lengths = list(final_key_length_data.keys())
    index_values = list(final_key_length_data.values())
    
    ax.bar(key_lengths, index_values, color='skyblue')
    ax.set_xlabel('Độ dài khóa (Key Length)')
    ax.set_ylabel('Chỉ số trùng khớp (IoC)')
    ax.set_title('Chỉ số trùng khớp cho mật mã cuối cùng')
    ax.set_xticks(key_lengths)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.axhline(y=0.067, color='r', linestyle='-', alpha=0.7, label='Dự kiến cho tiếng Anh')
    ax.legend()
    
    st.pyplot(fig)
    
    # Let the user try to break the cipher
    st.subheader("Công cụ phá mã")
    
    user_final_key_length = st.number_input("Nhập độ dài khóa bạn muốn thử:", min_value=1, max_value=15, value=6)
    
    if st.button("Phân tích với độ dài khóa này", key="analyze_final_key"):
        decrypted_text, discovered_key = break_vigenere_cipher(final_cipher, user_final_key_length)
        st.markdown(f"**Khóa có thể:** {discovered_key}")
        st.markdown(f"**Văn bản giải mã:**\n\n{decrypted_text}")
    
    # Final answer submission
    st.markdown("---")
    st.subheader("Gửi câu trả lời cuối cùng")
    
    final_key = st.text_input("Nhập khóa bạn đã phát hiện:", key="final_key")
    final_message = st.text_area("Nhập ý nghĩa chính của thông điệp (bằng tiếng Việt):", key="final_message")
    
    if st.button("Hoàn thành Thử thách", key="complete_final"):
        if final_key.upper() == "CIPHER" and "thông tin" in final_message.lower() and "bảo mật" in final_message.lower():
            st.session_state.final_challenge_completed = True
    
    # Display completion message and badge
    if st.session_state.final_challenge_completed:
        st.success("🎖️ CHÚC MỪNG! Bạn đã hoàn thành thử thách mật mã!")
        complete_challenge()
        
        # Display final badge
        badge_data = generate_badge("Chuyên Gia Mật Mã", "#1E88E5")
        st.markdown(f"""
        ## 🏆 Bạn đã trở thành Chuyên Gia Mật Mã!
        
        <img src="data:image/png;base64,{badge_data}" width="300">
        
        Bạn đã học được:
        1. Nguyên lý cơ bản của mật mã Vigenère
        2. Cách mã hóa và giải mã thông điệp
        3. Phân tích tần suất và kỹ thuật phá vỡ mật mã
        4. So sánh bảo mật giữa các phương pháp mã hóa khác nhau
        
        Hãy tiếp tục khám phá thế giới mật mã học!
        """, unsafe_allow_html=True)
        
        # Show snow animation
        st.snow()
        
        # Auto-show certificate after completion
        st.markdown("""
        <div style="text-align: center; margin-top: 30px;">
            <h2 style="color: #4CAF50;">🏆 Chứng nhận hoàn thành 🏆</h2>
            <div style="border: 3px solid #1E88E5; padding: 20px; margin: 20px auto; max-width: 600px; background-color: #f9f9f9;">
                <h3>Chứng nhận rằng</h3>
                <h2 style="color: #1E88E5; font-family: 'Arial', cursive;">Học sinh</h2>
                <p>đã thành công hoàn thành</p>
                <h3 style="color: #4CAF50;">Khóa học Mật mã Vigenère</h3>
                <p style="font-style: italic;">Ngày: 27/04/2025</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show error if incorrect
    elif final_key and final_message:
        st.error("Câu trả lời chưa chính xác. Hãy phân tích kỹ hơn và thử lại!")

def main():
    st.title(translations["title"])
    
    # Display game progress
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### {translations['level']}: {st.session_state.game_level}/4")
    with col2:
        st.markdown(f"### {translations['mission']}: {st.session_state.challenges_completed}/3")
    with col3:
        if st.session_state.mission_completed:
            st.markdown(f"### 🏆 {translations['mission_complete']}")
    
    # Show animations for achievements
    if st.session_state.show_animation:
        # Use Streamlit's native balloons
        st.balloons()
        st.session_state.show_animation = False
    
    # Display different content based on game level
    if st.session_state.game_level == 1:
        level_1_intro()
    elif st.session_state.game_level == 2:
        level_2_encryption_decryption()
    elif st.session_state.game_level == 3:
        level_3_breaking_cipher()
    elif st.session_state.game_level == 4:
        level_4_hacker_challenge()

if __name__ == "__main__":
    main()