# 🕵️‍♂️ Steganography – Hiding Information in the Image

This project demonstrates how to hide and extract secret messages inside an image using Python.  
It uses the **Least Significant Bit (LSB)** technique to embed text into image pixels without affecting the visible quality.

---

## 📌 Problem Statement

In today's digital age, secure transmission of sensitive data is essential.  
The challenge is to hide information in such a way that it does not attract attention or suspicion.  
This project solves this by hiding the message inside an image file.

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Pillow (PIL)** for image processing
- `os` module for file operations

---

## 🧠 Algorithm (LSB Steganography)

### 🔐 Encoding (Hiding Text)
1. Load the input image
2. Convert the message to binary
3. Modify the least significant bits of RGB pixels
4. Save the modified image as output

### 🔓 Decoding (Extracting Text)
1. Read LSBs from output image
2. Convert binary back to text
3. Stop when end marker (`###`) is found

---

## 📂 File Structure
