import tkinter as tk
from tkinter import ttk, scrolledtext
import re
import csv
import requests
from bs4 import BeautifulSoup

#Colors
BG_COLOR = "#e8f5e9"
PANEL_COLOR = "#c8e6c9"
BLUE_ACCENT = "#b3e5fc"
BUTTON_COLOR = "#66bb6a"
BUTTON_ACTIVE = "#43a047"
TEXT_COLOR = "#1b5e20"

# Buzzwords
buzzwords = ["eco-friendly", "natural", "green", "sustainable", "organic"]

# Fetch description from URL
def fetch_description_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        soup = BeautifulSoup(response.text, "html.parser")

        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            return meta.get("content")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        return text[:1500]

    except:
        return ""

# Clean text
def clean_text(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s.lower())

#CERTIFICATION CHECK
def check_certification(text, product_name):
    found_brands = []
    certs = []

    combined_text = text + " " + product_name
    cleaned_text = clean_text(combined_text)

    certification_keywords = [
        "fssai", "iso", "gmp", "fda", "ayush",
        "made safe", "b-corp", "cruelty free",
        "organic certified"
    ]

    detected_keywords = []

    for keyword in certification_keywords:
        if keyword in combined_text.lower():
            detected_keywords.append(keyword.upper())

    try:
        with open("brands.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                brand = row["Brand"]
                cleaned_brand = clean_text(brand)

                if cleaned_brand in cleaned_text or cleaned_text in cleaned_brand:
                    found_brands.append(brand)
                    certs.append(row["Certification"])

    except Exception as e:
        print("CSV ERROR:", e)

    all_certs = certs + detected_keywords

    return found_brands, list(set(all_certs))

#  Classifier
def classify_sentence(sentence):
    sentence = sentence.lower()

    if re.search(r'\d+%|\b(certified|iso|gots|b-corp|made safe|fssai|fda)\b', sentence):
        return "Evidence-Based"

    if any(word in sentence for word in buzzwords):
        return "Marketing Fluff"

    return "Neutral"

#  Audit
def audit_text():
    product_name = name_entry.get().strip()
    url = url_entry.get().strip()
    manual_text = input_text.get("1.0", tk.END).strip()

    text = ""

    if url != "":
        text = fetch_description_from_url(url)

    if text.strip() == "":
        text = manual_text

    if text.strip() == "":
        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "⚠️ Please enter a valid URL or description")
        output_box.config(state="disabled")
        return

    sentences = re.split(r'[.!?]', text)

    fluff_sentences = []
    evidence_sentences = []
    detected_buzzwords = set()  #  NEW

    for sentence in sentences:
        if sentence.strip() == "":
            continue

        lower_sentence = sentence.lower()

        # 🔍 Detect buzzwords
        for word in buzzwords:
            if word in lower_sentence:
                detected_buzzwords.add(word)

        category = classify_sentence(sentence)

        if category == "Marketing Fluff":
            fluff_sentences.append(sentence.strip())
        elif category == "Evidence-Based":
            evidence_sentences.append(sentence.strip())

    fluff_count = len(fluff_sentences)
    evidence_count = len(evidence_sentences)

    brands, certs = check_certification(text, product_name)

    verdict = "✅ Trustworthy" if evidence_count >= fluff_count else "❌ Not Trustworthy"

    reasoning = f"📦 Product: {product_name}\n"
    reasoning += f"🌐 Source: {'URL' if url else 'Manual Input'}\n"
    reasoning += f"\n🔎 Verdict: {verdict}\n"
    reasoning += f"📊 Fluff: {fluff_count} | Evidence: {evidence_count}\n\n"

    #  NEW: Explain WHY not trustworthy
    if verdict == "❌ Not Trustworthy" and detected_buzzwords:
        reasoning += "🚨 Reason: Heavy use of vague marketing buzzwords:\n"
        reasoning += "👉 " + ", ".join(detected_buzzwords) + "\n\n"

    if fluff_sentences:
        reasoning += "⚠️ Marketing Claims:\n"
        for s in fluff_sentences[:3]:
            reasoning += f"• {s}\n"

    if evidence_sentences:
        reasoning += "\n✅ Evidence Found:\n"
        for s in evidence_sentences[:3]:
            reasoning += f"• {s}\n"

    if brands:
        reasoning += f"\n🏷️ Brand Match: {brands}\n"

    if certs:
        reasoning += f"📜 Certifications: {certs}\n"
    else:
        reasoning += "\n❌ No certifications detected\n"

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, reasoning)
    output_box.config(state="disabled")

    table.insert("", "end", values=(product_name, verdict))

#  Clear fields
def clear_fields():
    name_entry.delete(0, tk.END)
    url_entry.delete(0, tk.END)
    input_text.delete("1.0", tk.END)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")

#  Clear table
def clear_table():
    for row in table.get_children():
        table.delete(row)

#  UI
root = tk.Tk()
root.title("🌱 Green Truth Auditor")
root.geometry("950x600")
root.configure(bg=BG_COLOR)

left_frame = tk.Frame(root, bg=PANEL_COLOR, bd=2, relief="ridge")
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = tk.Frame(root, bg=BG_COLOR)
right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

tk.Label(left_frame, text="🌿 Audit History",
         font=("Segoe UI", 13, "bold"),
         bg=PANEL_COLOR, fg=TEXT_COLOR).pack(pady=8)

columns = ("Product", "Status")
table = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)

table.heading("Product", text="Product")
table.heading("Status", text="Status")

table.column("Product", width=150, anchor="center")
table.column("Status", width=130, anchor="center")

table.pack(padx=5, pady=5)

tk.Button(left_frame, text="🧹 Clear Table",
          command=clear_table,
          bg="#81c784",
          fg="white",
          font=("Segoe UI", 10, "bold")).pack(pady=5)

tk.Label(right_frame, text="Green Truth Auditor",
         font=("Segoe UI", 16, "bold"),
         bg=BG_COLOR, fg="#0277bd").pack(pady=10)

tk.Label(right_frame, text="Product Name",
         font=("Segoe UI", 11, "bold"),
         bg=BG_COLOR, fg=TEXT_COLOR).pack()

name_entry = tk.Entry(right_frame, width=50, bg=BLUE_ACCENT)
name_entry.pack(pady=5)

tk.Label(right_frame, text="Product URL (optional)",
         font=("Segoe UI", 11, "bold"),
         bg=BG_COLOR, fg=TEXT_COLOR).pack()

url_entry = tk.Entry(right_frame, width=50, bg="#e1f5fe")
url_entry.pack(pady=5)

tk.Label(right_frame, text="Product Description",
         font=("Segoe UI", 11, "bold"),
         bg=BG_COLOR, fg=TEXT_COLOR).pack()

input_text = scrolledtext.ScrolledText(right_frame, width=65, height=8)
input_text.pack(pady=10)

btn_frame = tk.Frame(right_frame, bg=BG_COLOR)
btn_frame.pack()

tk.Button(btn_frame, text="🔍 Audit",
          command=audit_text,
          bg=BUTTON_COLOR, fg="white").pack(side="left", padx=5)

tk.Button(btn_frame, text="🧹 Clear",
          command=clear_fields,
          bg="#81c784", fg="white").pack(side="left", padx=5)

tk.Label(right_frame, text="Audit Result",
         font=("Segoe UI", 12, "bold"),
         bg=BG_COLOR, fg="#0277bd").pack(pady=5)

output_box = scrolledtext.ScrolledText(right_frame, width=65, height=12)
output_box.pack(pady=10)
output_box.config(state="disabled")

root.mainloop()