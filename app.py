from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

skills_required = ["python", "sql", "flask", "html"]

def extract_text(pdf_path):

    text = ""

    with open(pdf_path, "rb") as file:

        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:

            text += page.extract_text()

    return text.lower()

@app.route("/", methods=["GET", "POST"])

def index():

    match_percent = 0

    matched_skills = []

    if request.method == "POST":

        resume = request.files["resume"]

        path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume.filename
        )

        resume.save(path)

        text = extract_text(path)

        for skill in skills_required:

            if skill in text:

                matched_skills.append(skill)

        match_percent = (
            len(matched_skills)
            / len(skills_required)
        ) * 100

    return render_template(
        "index.html",
        match_percent=match_percent,
        matched_skills=matched_skills
    )

if __name__ == "__main__":

    app.run(debug=True)