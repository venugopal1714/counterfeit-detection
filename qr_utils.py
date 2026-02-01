import qrcode
import os

def generate_qr(product_id):
    print("QR FUNCTION CALLED FOR:", product_id)

    os.makedirs("static", exist_ok=True)
    img = qrcode.make(product_id)

    file_path = os.path.join("static", f"{product_id}.png")
    img.save(file_path)

    print("QR SAVED AT:", file_path)
