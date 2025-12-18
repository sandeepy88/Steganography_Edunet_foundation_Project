from PIL import Image
from cryptography.fernet import Fernet
import itertools

DELIMITER = "1111111111111110"


# ---------- KEY GENERATION ----------
def generate_key():
    return Fernet.generate_key()


# ---------- ENCRYPT ----------
def encrypt_message(message: str, key: bytes) -> str:
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())
    return ''.join(format(byte, '08b') for byte in encrypted) + DELIMITER


# ---------- DECRYPT ----------
def decrypt_message(binary_data: str, key: bytes) -> str:
    cipher = Fernet(key)
    byte_data = bytes(
        int(binary_data[i:i+8], 2)
        for i in range(0, len(binary_data), 8)
    )
    return cipher.decrypt(byte_data).decode()


# ---------- HIDE DATA ----------
def hide_data(input_img: str, output_img: str, message: str, key: bytes):
    img = Image.open(input_img).convert("RGB")
    pixels = list(img.getdata())

    binary_msg = encrypt_message(message, key)
    if len(binary_msg) > len(pixels):
        raise ValueError("Message too large for image")

    new_pixels = []
    msg_iter = iter(binary_msg)

    for pixel in pixels:
        try:
            bit = next(msg_iter)
            new_pixels.append((pixel[0] & ~1 | int(bit), pixel[1], pixel[2]))
        except StopIteration:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(output_img)
    print("✔ Data hidden successfully")


# ---------- EXTRACT DATA ----------
def extract_data(stego_img: str, key: bytes) -> str:
    img = Image.open(stego_img).convert("RGB")
    pixels = img.getdata()

    binary_data = "".join(str(pixel[0] & 1) for pixel in pixels)
    end = binary_data.find(DELIMITER)

    if end == -1:
        raise ValueError("No hidden data found")

    return decrypt_message(binary_data[:end], key)


# ---------- USAGE ----------
if __name__ == "__main__":
    key = generate_key()
    print("🔑 Key:", key)

    hide_data(
        input_img="input.png",
        output_img="output.png",
        message="Highly Secure Secret Message",
        key=key
    )

    secret = extract_data("output.png", key)
    print("🔓 Decrypted Message:", secret)
