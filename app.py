from flask import Flask, render_template, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def extract_text(pdf_path):
    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


def find_skills(text):

    skills_database = [
        
    "Python","SQL","Excel","Power BI","Tableau",
    "Statistics","Java","HTML","CSS","JavaScript",
    "Flask","Django","React","Node.js","MongoDB",
    "MySQL","PostgreSQL","Git","GitHub","AWS",
    "Machine Learning","Data Analysis","Pandas",
    "NumPy","C++","C","Bootstrap","Figma",
    "REST API","Linux"
]
    

    found_skills = []

    text = text.lower()

    for skill in skills_database:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


@app.route("/", methods=["GET", "POST"])
def home():
    resume_summary=""
    resume_text = ""
    found_skills = []
    missing_skills = []
    match_score = 0
    ats_score = 0
    recruiter_review = ""
    job_recommendations = []
    strengths = []
    weaknesses = []
    career_gap = ""
    predicted_role = "General"
    jd_match_score = 0
    missing_jd_skills = []
   
    

    if request.method == "POST":

        file = request.files["resume"]

        if file:

            path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(path)

            resume_text = extract_text(path)
            resume_summary = resume_text[:500]

            found_skills = find_skills(resume_text)

            job_description = request.form.get("job_description","")

            jd_match_score =0
            missing_jd_skills = []

            if job_description:
                jd_skills = find_skills(job_description)
                matched_jd_skills =[]

                for skill in jd_skills:
                    if skill in found_skills:
                        matched_jd_skills.append(skill)

                if len(jd_skills)>0:
                    jd_match_score=int(
                        len(matched_jd_skills)/len(jd_skills)*100)
                    
                for skill in jd_skills:
                    if skill not in found_skills:
                        missing_jd_skills.append(skill)
               
            

        if ("Python" in found_skills and
                "SQL" in found_skills and
               ("Power BI" in found_skills or "Excel" in found_skills)):

               predicted_role = "Data Analyst"

        elif ("HTML" in found_skills and "CSS" in found_skills):

              predicted_role = "Frontend Developer"

        elif ("Python" in found_skills and "Flask" in found_skills):

             predicted_role = "Python Developer"

        else:

            predicted_role = "General"
            # Role Based Skills

        if predicted_role == "Data Analyst":

           required_skills = [
                "Python",
                "SQL",
                "Excel",
                "Power BI",
                "Tableau",
                "Statistics"
    ]

        elif predicted_role == "Frontend Developer":

            required_skills = [
               "HTML",
               "CSS",
               "JavaScript",
               "React",
               "Git"
    ]

        elif predicted_role == "Python Developer":

            required_skills = [
               "Python",
               "Flask",
               "SQL",
               "Git"
    ]

    else:

       required_skills = found_skills


    matched = 0

    for skill in required_skills:
     if skill in found_skills:
        matched += 1

    if len(required_skills) > 0:
      match_score = int(
        matched / len(required_skills) * 100
    )
    else:
      match_score = 0

    for skill in required_skills:
    
        if skill not in found_skills:
          missing_skills.append(skill)

    ats_score = min(match_score + 20, 100)

    if match_score >= 80:
       recruiter_review = (
          "Excellent profile. Strong technical skills."
    )

    elif match_score >= 60:
        recruiter_review = (
        "Good profile. Add more industry-relevant skills."
    )

    else:
        recruiter_review = (
        "Profile needs improvement. Focus on missing skills."
    )


# Job Recommendations

    if "Python" in found_skills and "SQL" in found_skills:
        job_recommendations.append("Data Analyst")

    if "Python" in found_skills and "Flask" in found_skills:
        job_recommendations.append("Python Developer")

    if "HTML" in found_skills and "CSS" in found_skills:
        job_recommendations.append("Frontend Developer")

    if "Java" in found_skills:
        job_recommendations.append("Java Developer")


# Resume Strengths

    if len(found_skills) >= 5:
        strengths.append("Strong technical skill set")

    if "SQL" in found_skills:
     strengths.append("Database knowledge")

    if "Python" in found_skills:
      strengths.append("Programming skills")


# Weaknesses

    for skill in missing_skills:
        weaknesses.append("Missing " + skill)


# Career Gap Analysis

    if len(missing_skills) == 0:
        career_gap = "No major skill gaps found."

    else:
        career_gap = (
        "You should learn: "
        + ", ".join(missing_skills)
    )


    return render_template(
    "index.html",
    resume_text=resume_text,
    found_skills=found_skills,
    missing_skills=missing_skills,
    match_score=match_score,
    ats_score=ats_score,
    recruiter_review=recruiter_review,
    job_recommendations=job_recommendations,
    strengths=strengths,
    weaknesses=weaknesses,
    career_gap=career_gap,
    predicted_role=predicted_role,
    resume_summary=resume_summary,
    jd_match_score=jd_match_score,
    missing_jd_skills=missing_jd_skills
)
if __name__ == "__main__":
    print("Starting Flask App...")
    app.run(debug=True)

   