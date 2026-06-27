import os
from groq import Groq

def optimize_resume(resume_text, job_description, missing_skills):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    missing_str = ", ".join(missing_skills) if missing_skills else "none"

    prompt = f"""You are an expert resume writer and ATS optimization specialist. Rewrite and optimize the resume below to better match the job description.

CRITICAL STRUCTURE RULES (follow exactly):
1. KEEP the exact same section headers and section ORDER as the original resume. Do not add new sections, remove sections, or reorder them. If the original has "WORK EXPERIENCE" keep that exact wording, don't change it to "EXPERIENCE".
2. Write each section header in ALL CAPS on its own line.
3. Immediately after each section header, add a line containing only: ---
   (three dashes, nothing else) — this is a section divider.
4. Inside EXPERIENCE/INTERNSHIP sections: wrap the **company name** and **job title** in double asterisks for bold, e.g. **Senior Developer** at **TechCorp Inc.**
5. Inside EXPERIENCE/INTERNSHIP bullet points: wrap every specific tool, technology, framework, or programming language name in double asterisks for bold, e.g. "Built REST APIs using **Python**, **Flask**, and **PostgreSQL**".
6. Do NOT bold generic words, only bold actual proper nouns: company names, job titles, and named tools/technologies/frameworks/languages.
7. Keep all factual information (companies, dates, degrees, locations) exactly unchanged — only improve the wording, impact, and keyword relevance.
8. Naturally incorporate these missing keywords where genuinely relevant: {missing_str}
9. Make bullet points start with strong action verbs and include quantifiable impact where plausible.
10. Output ONLY the optimized resume text in the format described above — no preamble, no explanation, no markdown code fences.

JOB DESCRIPTION:
{job_description[:3000]}

ORIGINAL RESUME:
{resume_text[:4000]}

Now output the restructured, optimized resume following all rules above exactly:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2500,
        temperature=0.5,
    )

    return response.choices[0].message.content