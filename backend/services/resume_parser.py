import re
import pdfplumber
import docx

def parse_resume(filepath):
    text = ""
    if filepath.endswith(".pdf"):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"

    return {
        "raw_text": text,
        "skills":     _extract_skills(text),
        "email":      _extract_email(text),
        "phone":      _extract_phone(text),
        "education":  _extract_section(text, ["education", "qualification"]),
        "experience": _extract_section(text, ["experience", "employment", "work history"]),
        "projects":   _extract_section(text, ["projects", "project"]),
    }

def _extract_email(text):
    m = re.search(r'[\w.+-]+@[\w-]+\.\w+', text)
    return m.group() if m else ""

def _extract_phone(text):
    m = re.search(r'(\+?\d[\d\s\-().]{8,}\d)', text)
    return m.group().strip() if m else ""

def _extract_skills(text):
    SKILLS = [
        "python","java","javascript","typescript","c++","c#","go","rust","swift","kotlin",
        "react","angular","vue","node","flask","django","fastapi","spring","express",
        "sql","mysql","postgresql","mongodb","redis","sqlite","oracle",
        "aws","azure","gcp","docker","kubernetes","terraform","ci/cd","git","linux",
        "machine learning","deep learning","nlp","data science","tensorflow","pytorch",
        "html","css","rest","graphql","microservices","agile","scrum",
        "excel","power bi","tableau","pandas","numpy","scikit-learn",
    ]
    text_lower = text.lower()
    return [s for s in SKILLS if s in text_lower]

def _extract_section(text, keywords):
    lines = text.split("\n")
    result = []
    capturing = False
    for line in lines:
        ll = line.lower().strip()
        if any(kw in ll for kw in keywords) and len(ll) < 40:
            capturing = True
            continue
        if capturing:
            if ll and any(h in ll for h in ["education","experience","skills","projects","certifications","awards","summary","objective"]) and len(ll) < 40:
                break
            if line.strip():
                result.append(line.strip())
    return "\n".join(result[:20])
