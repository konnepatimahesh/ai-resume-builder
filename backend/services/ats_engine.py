import re
from services.resume_parser import parse_resume

COMMON_SKILLS = [
    "python","java","javascript","typescript","c++","c#","go","rust","swift","kotlin",
    "react","angular","vue","node","flask","django","fastapi","spring","express",
    "sql","mysql","postgresql","mongodb","redis","docker","kubernetes","git","linux",
    "aws","azure","gcp","machine learning","deep learning","nlp","data science",
    "tensorflow","pytorch","html","css","rest","graphql","agile","scrum",
    "excel","power bi","tableau","pandas","numpy","scikit-learn","ci/cd","terraform",
]

def analyze(filepath, job_description):
    parsed   = parse_resume(filepath)
    resume_text = parsed["raw_text"].lower()
    jd_lower    = job_description.lower()

    # Extract JD keywords
    jd_skills   = [s for s in COMMON_SKILLS if s in jd_lower]
    jd_words    = set(re.findall(r'\b\w{4,}\b', jd_lower)) - _stopwords()

    # Resume keywords
    resume_skills = parsed["skills"]
    resume_words  = set(re.findall(r'\b\w{4,}\b', resume_text))

    # Matched / missing skills
    matched_skills  = [s for s in jd_skills if s in resume_text]
    missing_skills  = [s for s in jd_skills if s not in resume_text]

    # Keyword overlap
    common_words    = jd_words & resume_words
    keyword_score   = min(len(common_words) / max(len(jd_words), 1) * 100, 100)

    # Skill score
    skill_score = (len(matched_skills) / max(len(jd_skills), 1)) * 100 if jd_skills else 50

    # Structure score
    structure_score = _structure_score(parsed["raw_text"])

    # Experience alignment
    exp_score = 70 if parsed["experience"] else 30

    # Final weighted score
    ats_score = (
        keyword_score * 0.35 +
        skill_score   * 0.35 +
        structure_score * 0.15 +
        exp_score     * 0.15
    )
    ats_score = round(min(ats_score, 100), 1)

    # Recommendations
    recommendations = _recommendations(missing_skills, parsed, ats_score)

    return {
        "ats_score":        ats_score,
        "matched_skills":   matched_skills,
        "missing_skills":   missing_skills[:10],
        "keyword_score":    round(keyword_score, 1),
        "skill_score":      round(skill_score, 1),
        "structure_score":  round(structure_score, 1),
        "recommendations":  recommendations,
        "resume_skills":    resume_skills,
        "parsed":           parsed,
    }

def _structure_score(text):
    score = 0
    sections = ["experience","education","skills","summary","projects","certifications"]
    text_lower = text.lower()
    for s in sections:
        if s in text_lower:
            score += 15
    return min(score, 100)

def _recommendations(missing_skills, parsed, score):
    recs = []
    if missing_skills:
        recs.append(f"Add these missing skills to your resume: {', '.join(missing_skills[:5])}")
    if not parsed["experience"]:
        recs.append("Add a clear Work Experience section with job titles, companies, and dates.")
    if not parsed["projects"]:
        recs.append("Add a Projects section to showcase practical experience.")
    if score < 60:
        recs.append("Use more keywords from the job description in your resume.")
    if score < 80:
        recs.append("Quantify your achievements with numbers (e.g. 'Improved performance by 30%').")
    recs.append("Use a clean single-column format for better ATS parsing.")
    recs.append("Start bullet points with strong action verbs (Built, Developed, Led, Optimized).")
    return recs

def _stopwords():
    return {"this","that","with","from","have","will","your","they","been","were",
            "their","what","when","which","would","could","should","about","into",
            "more","some","also","than","then","them","these","those","such","very"}
