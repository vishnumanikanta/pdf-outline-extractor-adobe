# PDF Outline Extractor – Adobe Connecting the Dots Challenge (Round 1A)

## 🔍 Overview
This solution extracts a structured outline from PDFs including:
- Title
- Headings (H1, H2, H3)
- Page numbers

## 🧠 Approach
- Uses `PyMuPDF` for parsing PDF structure and text
- Font size-based clustering to infer heading hierarchy
- First largest text = Title; next 3 largest font levels → H1, H2, H3

## 📦 How to Build and Run (Inside Docker)
```bash
# Build Docker image
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .

# Run Docker container
docker run --rm -v $(pwd)/app/input:/app/input -v $(pwd)/app/output:/app/output --network none pdf-outline-extractor:latest
```

## 📁 Folder Structure
- `app/input/` → Place all PDF files here
- `app/output/` → JSON outputs will be saved here
# pdf-outline-extractor-adobe
# pdf-persona-analyzer-adobe
