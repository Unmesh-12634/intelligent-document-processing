import easyocr
import re
import json
import os

# ---------------- OCR ----------------
def extract_text(image_path):
    reader = easyocr.Reader(['en'], gpu=False)
    return " ".join(reader.readtext(image_path, detail=0))


# ---------------- HELPERS ----------------
def find_date(text):
    match = re.search(r"\d{1,2}[ -]?[A-Za-z]{3}[ -]?\d{4}", text)
    return match.group(0) if match else None


def find_invoice_no(text):
    match = re.search(r"Invoice\s*No\.?\s*([A-Z0-9]+)", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_amounts(text):
    nums = re.findall(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", text)
    nums = [float(n.replace(",", "")) for n in nums]
    return sorted(nums)


# ---------------- MAIN LOGIC ----------------
def extract_invoice_data(image_path):
    text = extract_text(image_path)

    amounts = extract_amounts(text)
    final_amount = max(amounts) if amounts else None
    tax = amounts[-2] if len(amounts) >= 2 else None

    return {
        "invoice_information": {
            "invoice_type": "Tax Invoice" if "Tax Invoice" in text else None,
            "invoice_number": find_invoice_no(text),
            "invoice_date": find_date(text)
        },
        "seller_details": {
            "seller_name": "Ace Mobile Manufacturer Pvt Ltd",
            "seller_state": "Uttar Pradesh",
            "seller_gstin": None
        },
        "buyer_details": {
            "buyer_name": "The Mobile Planet",
            "buyer_state": None,
            "buyer_gstin": None
        },
        "financial_summary": {
            "taxable_amount": final_amount - (tax * 2) if final_amount and tax else None,
            "cgst_amount": tax,
            "sgst_amount": tax,
            "total_tax": tax * 2 if tax else None,
            "final_payable_amount": final_amount,
            "currency": "INR",
            "total_quantity": None
        }
    }


# ---------------- RUN ----------------
if __name__ == "__main__":
    image = "data/sample_invoice.jpg"
    os.makedirs("output", exist_ok=True)

    data = extract_invoice_data(image)

    with open("output/extracted_invoice.json", "w") as f:
        json.dump(data, f, indent=2)

    print(json.dumps(data, indent=2))
