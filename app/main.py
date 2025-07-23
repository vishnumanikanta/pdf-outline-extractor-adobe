import fitz  # PyMuPDF
import os
import json

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []
    font_stats = {}

    for page_number in range(len(doc)):
        page = doc[page_number]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = ""
                max_font_size = 0
                for span in line["spans"]:
                    line_text += span["text"].strip()
                    if span["size"] > max_font_size:
                        max_font_size = span["size"]
                    font_key = round(span["size"], 1)
                    font_stats[font_key] = font_stats.get(font_key, 0) + 1
                if line_text:
                    headings.append({
                        "text": line_text,
                        "font_size": round(max_font_size, 1),
                        "page": page_number + 1
                    })

    # Sort font sizes to determine hierarchy
    sorted_fonts = sorted(font_stats.items(), key=lambda x: x[0], reverse=True)
    font_to_level = {}
    if sorted_fonts:
        font_to_level[sorted_fonts[0][0]] = "title"
        if len(sorted_fonts) > 1:
            font_to_level[sorted_fonts[1][0]] = "H1"
        if len(sorted_fonts) > 2:
            font_to_level[sorted_fonts[2][0]] = "H2"
        if len(sorted_fonts) > 3:
            font_to_level[sorted_fonts[3][0]] = "H3"

    output = {
        "title": "",
        "outline": []
    }

    for item in headings:
        level = font_to_level.get(item["font_size"])
        if level == "title" and output["title"] == "":
            output["title"] = item["text"]
        elif level in {"H1", "H2", "H3"}:
            output["outline"].append({
                "level": level,
                "text": item["text"],
                "page": item["page"]
            })

    return output

def main():
    input_folder = "/app/input"
    output_folder = "/app/output"
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_data = extract_outline_from_pdf(input_path)
            json_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_folder, json_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
