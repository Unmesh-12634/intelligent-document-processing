# Intelligent Document Processing (IDP) Internship Assignment

This project is a Python-based Intelligent Document Processing (IDP) solution designed to extract structured data from invoices. It utilizes **EasyOCR** for optical character recognition and a custom rule-based engine for cleaning and validating extracted fields.

## 📌 Project Overview

The system automates the extraction of key invoice details, including:
-   **Invoice Number & Date**
-   **Seller & Buyer Details**
-   **Financial Summaries** (Taxable Amount, Tax, Total Payable)

It handles common OCR noise (e.g., typos in "Uttar Pradesh", malformed dates) and outputs a strictly formatted JSON file ready for downstream processing.

## 📂 Project Structure

```
intelligent-document-processing/
├── data/
│   └── sample_invoice.jpg       # Input invoice image
├── output/
│   └── extracted_invoice.json   # Generated JSON output
├── src/
│   └── main.py                  # Core extraction script
├── README.md                    # Documentation
└── requirements.txt             # Project dependencies
```

## 🛠️ Tools & Technologies

-   **Language**: Python 3.x
-   **OCR Engine**: `EasyOCR` (chosen for its robustness on scene text and document headers)
-   **Image Processing**: `OpenCV` (headless backend)
-   **Data Processing**: Regular Expressions (`re`) for pattern parsing

## 🚀 How to Run

1.  **Extract the project** to your local machine.
2.  **Open a terminal** inside the project folder.
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Script**:
    ```bash
    python src/main.py
    ```
    *Note: The script defaults to processing `data/sample_invoice.jpg`. You can also pass a file path: `python src/main.py my_invoice.jpg`.*

5.  **View Output**:
    -   The extracted data will be printed to the **console**.
    -   A valid JSON file will be saved to **`output/extracted_invoice.json`**.

## 🧠 Approach & Logic

1.  **Text Extraction**: The image is processed using EasyOCR with English language models.
2.  **Keyword Anchoring**: We identify key sections using anchors like "Tax Invoice", "GSTIN", and "Total".
3.  **Heuristic Parsers**:
    -   **Dates**: Regex handles OCR anomalies (e.g., correcting "209" to "2019").
    -   **Amounts**: Financials are parsed by standardizing commas/decimals and identifying the largest value as the "Final Payable".
4.  **Strict Validation**:
    -   **State Cleaning**: "Uttar Pradesh Code Terms" is strictly cleaned to "Uttar Pradesh".
    -   **Null Enforcement**: Fields that are unreliable or explicitly excluded (like specific addresses or empty GSTINs) are forced to `null` to ensure data integrity.

## 💡 Future Improvements with NLP / LLMs

*Response to Internship Evaluation Question:*

While the current regex-based approach is efficient for fixed templates, it can be brittle. To improve accuracy and handle diverse layouts, I would integrate **NLP and LLMs** in the following ways:

1.  **LayoutLM (Document Understanding)**:
    -   Instead of relying on text proximity, I would use a multi-modal model like **LayoutLMv3**. It understands that text in the top-right is likely a date, purely based on 2D position and visual layout, vastly outperforming regex on unseen templates.

2.  **Named Entity Recognition (NER)**:
    -   I would train a **spaCy** or **HuggingFace** pipeline to specifically recognize `ORG` (Organizations) and `MONEY` tokens. This context-aware extraction is more robust than looking for keywords like "Pvt Ltd".

3.  **Generative AI / LLM Correction**:
    -   **Post-Processing**: I would feed the raw OCR output into a lightweight LLM (like Gemini Flash or GPT-4o-mini) with a prompt to "Correct typos and format to JSON". This is incredibly effective at fixing semantic errors (e.g., "18 APL 209" -> "18-Apr-2019") that regex often misses.

---
*Submitted by Unmesh joshi for the AI Research Internship.*
