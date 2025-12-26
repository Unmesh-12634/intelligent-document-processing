import cv2
import pytesseract
import re
import json
import os

# ---------------- TESSERACT PATH ----------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ================= IMAGE PREPROCESSING =================
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Resize
    img = cv2.resize(img, None, fx=1.7, fy=1.7, interpolation=cv2.INTER_CUBIC)

    # Noise removal
    img = cv2.medianBlur(img, 5)

    # Adaptive threshold (best for handwriting)
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Morphology to connect broken letters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    return img


# ================= OCR =================
def extract_raw_text(image_path):
    img = preprocess_image(image_path)
    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(img, config=config)
    return text


# ================= TEXT CLEANING =================
def clean_ocr_text(text):
    cleaned_lines = []
    for line in text.split("\n"):
        line = line.strip()

        # Remove unwanted characters
        line = re.sub(r"[^A-Za-z0-9 ₹:/.-]", "", line)

        # Ignore very small junk lines
        if len(line) < 3:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


# ================= ENTITY EXTRACTION =================
def extract_shop_name(text):
    for line in text.split("\n"):
        if line.isupper() and len(line) > 15:
            return line.strip()
    return None


def extract_bill_number(text):
    for line in text.split("\n"):
        if "No" in line or "NO" in line:
            nums = re.findall(r"\d+", line)
            if nums:
                return nums[0]
    return None


def extract_items(text):
    items = []
    for line in text.split("\n"):
        match = re.search(r"([A-Za-z ]{3,})\s+(\d{1,4})$", line)
        if match:
            name = match.group(1).strip()
            price = int(match.group(2))

            # Validation
            if price > 5:
                items.append({
                    "item": name,
                    "price": price
                })
    return items


def extract_total(text):
    # Keyword-based extraction
    match = re.search(r"(Total|Tota|Amt|Net)\s*[:\-]?\s*(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(2))

    # Fallback: largest number
    nums = re.findall(r"\b\d+\b", text)
    nums = [int(n) for n in nums if int(n) > 10]
    return max(nums) if nums else None


# ================= MAIN LOGIC =================
def extract_bill_data(image_path):
    raw_text = extract_raw_text(image_path)
    clean_text = clean_ocr_text(raw_text)

    print("\n----- RAW OCR TEXT -----\n")
    print(raw_text)

    print("\n----- CLEANED OCR TEXT -----\n")
    print(clean_text)

    final_data = {
        "shop_name": extract_shop_name(clean_text),
        "bill_number": extract_bill_number(clean_text),
        "items": extract_items(clean_text),
        "total_amount": extract_total(clean_text),
        "currency": "INR"
    }

    return final_data


# ================= RUN =================
if __name__ == "__main__":
    image_path = "data/good-hand-written-bill.jpg"

    os.makedirs("output", exist_ok=True)

    result = extract_bill_data(image_path)

    print("\n----- FINAL CLEAN OUTPUT -----\n")
    print(json.dumps(result, indent=2))

    with open("output/final_bill.json", "w") as f:
        json.dump(result, f, indent=2)
