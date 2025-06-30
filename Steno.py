from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def encode_image(img_path, secret_text, output_path):
    img = Image.open(img_path)
    binary_secret = text_to_bin(secret_text + "###")  # End marker
    data_index = 0
    pixels = img.getdata()
    new_pixels = []

    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(3):  # RGB channels
            if data_index < len(binary_secret):
                new_pixel[i] = new_pixel[i] & ~1 | int(binary_secret[data_index])
                data_index += 1
        new_pixels.append(tuple(new_pixel))

    img.putdata(new_pixels)
    img.save(output_path)
    print("✅ Data encoded successfully in", output_path)

def decode_image(img_path):
    img = Image.open(img_path)
    pixels = img.getdata()
    binary_data = ''

    for pixel in pixels:
        for i in range(3):
            binary_data += str(pixel[i] & 1)

    text = bin_to_text(binary_data)
    return text.split("###")[0]  # Stop at marker

# Example testing
# encode_image("input.png", "Secret message from RC Explore!", "output.png")
# print("Decoded:", decode_image("output.png"))
