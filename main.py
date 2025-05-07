import streamlit as st
import numpy as np
import cv2
import math
from io import BytesIO
from PIL import Image

# Constants
BITS = 2
HIGH_BITS = 256 - (1 << BITS)
LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'


def encode(block, data):
    data = ord(data)
    for idx in range(len(block)):
        block[idx] &= HIGH_BITS
        block[idx] |= (data >> (BITS * idx)) & LOW_BITS


def decode(block):
    val = 0
    for idx in range(len(block)):
        val |= (block[idx] & LOW_BITS) << (idx * BITS)
    return chr(val)


def insert(img, txt):
    ori_shape = img.shape
    max_bytes = ori_shape[0] * ori_shape[1] // BYTES_PER_BYTE
    txt = '{}{}{}'.format(len(txt), FLAG, txt)
    assert max_bytes >= len(txt), "Message overflow the capacity: {}".format(max_bytes)

    data = np.reshape(img, -1)
    for idx, val in enumerate(txt):
        encode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE], val)
    return np.reshape(data, ori_shape)


def extract(img):
    data = np.reshape(img, -1)
    total = data.shape[0]
    res = ''
    idx = 0

    while idx < total // BYTES_PER_BYTE:
        ch = decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE])
        idx += 1
        if ch == FLAG:
            break
        res += ch

    end = int(res) + idx
    assert end <= total // BYTES_PER_BYTE, "Input image isn't correct."

    res = ''
    while idx < end:
        res += decode(data[idx * BYTES_PER_BYTE: (idx + 1) * BYTES_PER_BYTE])
        idx += 1
    return res


# Streamlit UI
st.title("🔐 LSB Steganography - Embed and Extract Text from Image")

tab1, tab2 = st.tabs(["📥 Embed Message", "📤 Extract Message"])

with tab1:
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    st.image()
    secret_text = st.text_area("Enter the secret message to embed")

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
        image_np = np.array(image)

        if st.button("🔏 Embed and Download"):
            try:
                stego_img_np = insert(image_np.copy(), secret_text)
                stego_img = Image.fromarray(stego_img_np.astype('uint8'))
                buf = BytesIO()
                stego_img.save(buf, format="PNG")
                byte_im = buf.getvalue()
                st.success("Message embedded successfully!")
                st.download_button(
                    label="⬇ Download Image with Message",
                    data=byte_im,
                    file_name="image_with_message.png",
                    mime="image/png"
                )
            except AssertionError as e:
                st.error(str(e))

with tab2:
    uploaded_stego_file = st.file_uploader(
        "Upload a stego image to extract", type=["png", "jpg", "jpeg"], key="extract"
    )

    if uploaded_stego_file is not None:
        stego_image = Image.open(uploaded_stego_file).convert('RGB')
        st.image()
        stego_np = np.array(stego_image)

        if st.button("📤 Extract Message"):
            try:
                message = extract(stego_np)
                st.success("Message extracted:")
                st.code(message)
            except Exception as e:
                st.error(f"Error extracting message: {e}")
