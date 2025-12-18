from PIL import Image
from cryptography.fernet import Fernet

# Generate key (run once & save it)
key = Fernet.generate_key()
cipher = Fernet(key)

print("Encryption Key:", key)

def hide_data(image_path, message, output_image):
    encrypted_msg = cipher.encrypt(message.encode())
    binary_msg = ''.join(format(byte, '08b') for byte in encrypted_msg) + '1111111111111110'

    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size
    data_index = 0

    for y in range(height):
        for x in range(width):
            if data_index < len(binary_msg):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_msg[data_index])
                pixels[x, y] = (r, g, b)
                data_index += 1

    img.save(output_image)
    print("Data hidden successfully!")

# Example
hide_data("input.png", "Secret Message Here", "output.png")


---

 2. Extract + Decrypt Data from Image

def extract_data(image_path, key):
    cipher = Fernet(key)
    img = Image.open(image_path)
    pixels = img.load()

    binary_data = ""
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)

    bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    encrypted_msg = bytes(int(b, 2) for b in bytes_data)

    decrypted_msg = cipher.decrypt(encrypted_msg)
    return decrypted_msg.decode()

# Example
secret = extract_data("output.png", key)
print("Hidden Message:", secret)

