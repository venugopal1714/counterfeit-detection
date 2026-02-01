from flask import Flask, render_template, request
from blockchain import Blockchain
from qr_utils import generate_qr

app = Flask(__name__)
blockchain = Blockchain()

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        product_id = request.form["product_id"]
        product_name = request.form["product_name"]

        print("REGISTERING:", product_id, product_name)

        blockchain.add_block({
            "product_id": product_id,
            "product_name": product_name
        })

        generate_qr(product_id)

        return f"Product Registered. QR saved as static/{product_id}.png"

    return render_template("register.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    result = None
    if request.method == "POST":
        product_id = request.form["product_id"]

        exists = any(
            isinstance(b.data, dict) and b.data.get("product_id") == product_id
            for b in blockchain.chain
        )

        if blockchain.is_chain_valid() and exists:
            result = "✅ AUTHENTIC PRODUCT"
        else:
            result = "❌ FAKE OR TAMPERED PRODUCT"

    return render_template("verify.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
