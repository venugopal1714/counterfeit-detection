import qrcode
import os
import json
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


def generate_qr(product_id, block_hash):
    os.makedirs(STATIC_DIR, exist_ok=True)

    qr_data = {
        "product_id": product_id,
        "block_hash": block_hash
    }

    img = qrcode.make(json.dumps(qr_data))
    img.save(os.path.join(STATIC_DIR, f"{product_id}.png"))


def decode_qr(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if not data:
        return None

    return json.loads(data)
