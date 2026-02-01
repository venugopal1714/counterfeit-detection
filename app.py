from flask import Flask, render_template, request
import os

from blockchain import Blockchain
from qr_utils import generate_qr, decode_qr
from db import init_db, add_product, get_product, log_verification

app = Flask(__name__)

# Initialize core components
blockchain = Blockchain()
init_db()

UPLOAD_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -------------------------
# REGISTER PRODUCT
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        product_id = request.form["product_id"]
        product_name = request.form["product_name"]

        # Add product to blockchain
        blockchain.add_block({
            "product_id": product_id,
            "product_name": product_name
        })

        # Get blockchain proof
        block_hash = blockchain.chain[-1].hash

        # Store in database
        add_product(product_id, product_name, block_hash)

        # Generate QR
        generate_qr(product_id, block_hash)

        return render_template(
            "register_success.html",
            product_id=product_id
        )

    return render_template("register.html")


# -------------------------
# VERIFY PRODUCT
# -------------------------
@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        product_id = request.form["product_id"]
        qr_file = request.files.get("qr_image")

        if not qr_file:
            return render_template(
                "result.html",
                status="FAKE",
                product_id=product_id
            )

        qr_path = os.path.join(UPLOAD_DIR, "temp_qr.png")
        qr_file.save(qr_path)

        try:
            qr_data = decode_qr(qr_path)
        except Exception:
            log_verification(product_id, "FAKE")
            return render_template(
                "result.html",
                status="FAKE",
                product_id=product_id
            )

        if not qr_data:
            log_verification(product_id, "FAKE")
            return render_template(
                "result.html",
                status="FAKE",
                product_id=product_id
            )

        db_product = get_product(product_id)

        if not db_product:
            log_verification(product_id, "FAKE")
            status = "FAKE"

        elif qr_data.get("product_id") != product_id:
            log_verification(product_id, "FAKE")
            status = "FAKE"

        elif qr_data.get("block_hash") != db_product[2]:
            log_verification(product_id, "FAKE")
            status = "FAKE"

        elif not blockchain.is_chain_valid():
            log_verification(product_id, "TAMPERED")
            status = "TAMPERED"

        else:
            log_verification(product_id, "AUTHENTIC")
            status = "AUTHENTIC"

        return render_template(
            "result.html",
            status=status,
            product_id=product_id
        )

    return render_template("verify.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
