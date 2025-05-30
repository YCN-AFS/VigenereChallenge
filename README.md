# Vigenère Cipher Challenge 🔐🧩

## 📝 Overview

The Vigenère Cipher Challenge is an interactive educational Streamlit application designed to provide an engaging and comprehensive learning experience about the Vigenère Cipher, a classic encryption technique. This project aims to help users understand cryptography principles through hands-on challenges and interactive tools.

## ✨ Features

- 🔒 Interactive Vigenère Cipher learning
- 🔤 Encryption and decryption challenges
- 📊 Frequency analysis tools
- 🌐 Multilingual support (Vietnamese)

## 🛠 Technologies Used

- [Streamlit](https://streamlit.io/): Web application framework
- [Python](https://www.python.org/): Primary programming language
- [Matplotlib](https://matplotlib.org/): Data visualization
- [Pillow](https://python-pillow.org/): Image processing
- [Googletrans](https://py-googletrans.readthedocs.io/): Translation support

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/) (optional)

## 🔧 Installation and Running

### Option 1: Docker

1. Build the Docker image:
```bash
docker build -t vigenere-cipher-challenge .
```

2. Run the Docker container:
```bash
docker run -p 8501:8501 vigenere-cipher-challenge
```

3. Open your web browser and navigate to:
```
http://localhost:8501
```

### Option 2: Docker Compose (Optional)

1. Create a `docker-compose.yml` file:
```yaml
version: '3'
services:
  app:
    build: .
    ports:
      - "8501:8501"
```

2. Run the application:
```bash
docker-compose up
```

## 📚 Learning Objectives

- Understand the principles of the Vigenère Cipher
- Learn encryption and decryption techniques
- Explore cryptographic analysis methods
- Practice breaking classical encryption systems

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📜 License

[Add your license information here]

## 🏆 Acknowledgments

- Inspired by classical cryptography techniques
- Special thanks to the open-source community
