"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def get_homepage():
    """Display lists of all students and all projects"""

    students = hackbright.get_all_students()
    projects = hackbright.get_all_projects()

    return render_template("homepage.html",
                           students=students,
                           projects=projects)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student/")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    grades = hackbright.get_grades_by_github(github)

    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           grades=grades)


@app.route("/student-add")
def add_student_form():
    """Show form for adding a student."""

    return render_template("student_add_form.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("confirmation.html", first=first, last=last,
                           github=github)


@app.route("/project/<title>")
def show_project_details(title):
    """Display project details: title, description, maximum grade."""

    title, description, max_grade = hackbright.get_project_by_title(title)

    student_grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           student_grades=student_grades)


@app.route("/project-add")
def add_project_form():
    """Show form for adding a project."""

    return render_template("project_add_form.html")


@app.route("/project-add", methods=['POST'])
def project_add():
    """Add a project."""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return render_template("project_add_confirmation.html", title=title)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
