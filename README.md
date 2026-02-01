# 🔐 QR-Based Counterfeit Detection System using Simulated Blockchain

A web-based application to **detect counterfeit products** using **QR code verification** and a **simulated blockchain** for tamper-resistant traceability.  
The system allows users to register products, generate QR codes, and verify product authenticity in real time.

🚀 **Live Demo:** https://counterfeit-detection-m5vy.onrender.com 
📦 **Tech Stack:** Flask | SQLite | QR Codes | SHA-256 Blockchain | Render

---

## 📌 Problem Statement

Counterfeit products are a major issue across industries, leading to financial loss and safety risks.  
Traditional verification systems are often centralized and easy to tamper with.

This project addresses the problem by:
- Assigning a **unique QR code** to each product
- Storing product proof using **blockchain-style hash chaining**
- Verifying authenticity by validating QR data, database records, and blockchain integrity

---

## 🏗️ System Architecture
User
│
│ Register / Verify
▼
Flask Web Application
│
├── QR Code Generator & Decoder
├── SQLite Database (Product Records & Logs)
├── Simulated Blockchain (SHA-256 Hash Chain)
│
▼
Verification Result (AUTHENTIC / FAKE / TAMPERED)


### Core Components
- **Frontend:** HTML, Bootstrap
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Blockchain:** Custom SHA-256 hash chaining
- **Deployment:** Render (Cloud Web Service)

---

## ✨ Features

- ✅ Product registration with unique product ID
- 🧾 Automatic QR code generation
- 🔎 QR upload–based product verification
- 🔗 Blockchain integrity validation
- 🚫 Detects fake or tampered products
- 🌍 Publicly deployed and accessible

---

## 🛠️ Technologies Used

| Category | Technology |
|--------|-----------|
| Backend | Python, Flask |
| Database | SQLite |
| Blockchain | SHA-256 Hash Chaining |
| QR Code | qrcode, OpenCV |
| Frontend | HTML, Bootstrap |
| Deployment | Render |

---

## ▶️ How It Works

### 1️⃣ Product Registration
- User enters product ID and product name
- A new block is added to the blockchain
- A QR code is generated containing:
  - Product ID
  - Blockchain block hash
- Product details are stored in SQLite

### 2️⃣ Product Verification
- User uploads the QR code image
- The system decodes QR data
- Verification checks:
  - Product exists in the database
  - QR data matches stored product data
  - Blockchain integrity is intact
- Result is displayed as:
  - **AUTHENTIC**
  - **FAKE**
  - **TAMPERED**

---

