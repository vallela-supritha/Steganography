# Steganography

````markdown
# 🔐 LSB Steganography Web App

A simple and interactive web application built using **Streamlit** that allows you to embed (encode) and extract (decode) secret messages in images using **Least Significant Bit (LSB)** steganography.

## 🚀 Features

- 📥 Embed Messages:Hide secret text inside an image using LSB technique.
- 📤 Extract Messages:Retrieve the hidden message from a stego image.
- 🖼️ Supports PNG, JPG, and JPEG formats.
- 💡 Built with an intuitive and responsive user interface using **Streamlit**.
- 🔐 Uses 2-bit encoding per byte for efficient data embedding.

## 🧠 How It Works

- The app uses 2 bits of each pixel channel (R, G, B) to store parts of the secret message.
- The message is prefixed with its length followed by a special delimiter `%` for secure retrieval.
- Encoding: Converts text characters into binary and embeds them in the image pixel data.
- Decoding: Reconstructs the text from the modified image using the embedded length.

## 📦 Tech Stack

- Python
- Streamlit
- NumPy
- OpenCV
- Pillow (PIL)

````

## 🏁 Future Improvements

* Support for larger messages with compression.
* Encryption layer before embedding.
* Drag-and-drop UI for uploading files.

## 🙋‍♀️ Author

Supritha Vallella
🔗 [Portfolio](https://supritha735.netlify.app) | 🌐 [LinkedIn]([https://www.linkedin.com](https://www.linkedin.com/in/supritha-vallela-b8b4322a2/) | 🐍 [HackerRank]([https://www.hackerrank.com](https://www.hackerrank.com/profile/supritha_vallela)

