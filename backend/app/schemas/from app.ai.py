from app.ai.pdf_analyzer import PDFAnalyzer

text = PDFAnalyzer.extract_text("uploads/Resume.pdf")

print(text)