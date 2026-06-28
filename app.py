from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = "smart_student_2024"

DATA_FILE = os.path.join(os.path.dirname(__file__), "students.txt")


# ─── File helpers ────────────────────────────────────────────────────────────

def read_students():
    students = []
    if not os.path.exists(DATA_FILE):
        return students
    with open(DATA_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 5:
                try:
                    students.append({
                        "id": int(parts[0]),
                        "name": parts[1],
                        "age": int(parts[2]),
                        "grade": parts[3],
                        "marks": int(parts[4])
                    })
                except ValueError:
                    pass
    return students


def write_students(students):
    with open(DATA_FILE, "w") as f:
        for s in students:
            f.write(f"{s['id']},{s['name']},{s['age']},{s['grade']},{s['marks']}\n")


def validate_student(data, existing_ids=None, update_id=None):
    errors = []
    # ID
    try:
        sid = int(data.get("id", ""))
        if sid <= 0:
            errors.append("ID must be a positive integer.")
        elif existing_ids is not None and sid in existing_ids and sid != update_id:
            errors.append(f"ID {sid} already exists.")
    except (ValueError, TypeError):
        errors.append("ID must be a valid integer.")
    # Name
    name = data.get("name", "").strip()
    if not name:
        errors.append("Name cannot be empty.")
    elif name.isnumeric():
        errors.append("Name cannot be purely numeric.")
    # Age
    try:
        age = int(data.get("age", ""))
        if age <= 0:
            errors.append("Age must be greater than 0.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid integer.")
    # Grade
    grade = data.get("grade", "").strip().upper()
    if grade not in list("ABCDEF"):
        errors.append("Grade must be a single uppercase letter A–F.")
    # Marks
    try:
        marks = int(data.get("marks", ""))
        if not (0 <= marks <= 100):
            errors.append("Marks must be between 0 and 100.")
    except (ValueError, TypeError):
        errors.append("Marks must be a valid integer.")
    return errors


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    students = read_students()
    return render_template("index.html", students=students, count=len(students))


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        data = request.form.to_dict()
        students = read_students()
        existing_ids = {s["id"] for s in students}
        errors = validate_student(data, existing_ids)
        if errors:
            return jsonify({"success": False, "errors": errors})
        students.append({
            "id": int(data["id"]),
            "name": data["name"].strip(),
            "age": int(data["age"]),
            "grade": data["grade"].strip().upper(),
            "marks": int(data["marks"])
        })
        write_students(students)
        return jsonify({"success": True, "message": f"Student {data['name'].strip()} added successfully!"})
    return render_template("add.html")


@app.route("/students")
def view_students():
    students = read_students()
    return render_template("students.html", students=students, count=len(students))


@app.route("/search")
def search_student():
    query = request.args.get("q", "").strip().lower()
    students = read_students()
    results = []
    if query:
        for s in students:
            if query == str(s["id"]) or query in s["name"].lower():
                results.append(s)
    return render_template("search.html", results=results, query=query, searched=bool(query))


@app.route("/update/<int:sid>", methods=["GET", "POST"])
def update_student(sid):
    students = read_students()
    student = next((s for s in students if s["id"] == sid), None)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("view_students"))
    if request.method == "POST":
        data = request.form.to_dict()
        data["id"] = sid
        existing_ids = {s["id"] for s in students}
        errors = validate_student(data, existing_ids, update_id=sid)
        if errors:
            return jsonify({"success": False, "errors": errors})
        for s in students:
            if s["id"] == sid:
                s["name"] = data["name"].strip()
                s["age"] = int(data["age"])
                s["grade"] = data["grade"].strip().upper()
                s["marks"] = int(data["marks"])
        write_students(students)
        return jsonify({"success": True, "message": "Student updated successfully!"})
    return render_template("update.html", student=student)


@app.route("/delete/<int:sid>", methods=["POST"])
def delete_student(sid):
    students = read_students()
    new_students = [s for s in students if s["id"] != sid]
    if len(new_students) == len(students):
        return jsonify({"success": False, "message": "Student not found."})
    write_students(new_students)
    return jsonify({"success": True, "message": "Student deleted successfully."})


@app.route("/analytics")
def analytics():
    students = read_students()
    if not students:
        return render_template("analytics.html", data=None)
    marks_list = [s["marks"] for s in students]
    avg = round(sum(marks_list) / len(marks_list), 2)
    top = max(students, key=lambda s: s["marks"])
    below_avg = [s for s in students if s["marks"] < avg]
    highest = max(marks_list)
    lowest = min(marks_list)
    grade_dist = {}
    for s in students:
        grade_dist[s["grade"]] = grade_dist.get(s["grade"], 0) + 1
    pass_rate = round(len([s for s in students if s["marks"] >= 50]) / len(students) * 100, 1)
    age_avg = round(sum(s["age"] for s in students) / len(students), 1)
    data = {
        "avg": avg,
        "top": top,
        "below_avg_count": len(below_avg),
        "highest": highest,
        "lowest": lowest,
        "grade_dist": grade_dist,
        "pass_rate": pass_rate,
        "age_avg": age_avg,
        "total": len(students),
        "marks_list": marks_list,
        "names": [s["name"] for s in students]
    }
    return render_template("analytics.html", data=data)


# ─── Chatbot ─────────────────────────────────────────────────────────────────

CHAT_RESPONSES = {
    "add": {
        "keywords": ["add", "insert", "create", "new student", "register"],
        "answer": "To <b>add a student</b>, click <b>Add Student</b> in the navbar or sidebar. Fill in the ID (unique integer), full name, age, grade (A–F), and marks (0–100). All fields are validated before saving. The record is stored in <code>students.txt</code> automatically."
    },
    "view": {
        "keywords": ["view", "see", "list", "all students", "show"],
        "answer": "Click <b>All Students</b> in the menu to see every record in a sortable table. The total count is shown at the top. You can also <b>edit</b> or <b>delete</b> any student directly from that table."
    },
    "search": {
        "keywords": ["search", "find", "look", "query"],
        "answer": "Use the <b>Search</b> page to find a student by their <b>ID</b> or part of their <b>name</b> (case-insensitive). Type your query and press Enter — matching records appear instantly."
    },
    "update": {
        "keywords": ["update", "edit", "change", "modify"],
        "answer": "To update a student, go to <b>All Students</b>, find the record, and click the <b>Edit</b> (pencil) icon. A pre-filled form opens — change any field and click Save. The file is rewritten with the new data."
    },
    "delete": {
        "keywords": ["delete", "remove", "erase"],
        "answer": "Click the <b>Delete</b> (trash) icon next to a student in the list. A confirmation dialog appears before any data is removed, so you won't delete by accident."
    },
    "analytics": {
        "keywords": ["analytic", "analysis", "average", "top", "chart", "stats", "grade", "performance"],
        "answer": "The <b>Analytics</b> page shows: average marks, top performer, students below average, highest & lowest scores, grade distribution chart, pass rate, and average age. Navigate there from the sidebar."
    },
    "grade": {
        "keywords": ["grade", "a b c d e f", "grading"],
        "answer": "Grades accepted are <b>A, B, C, D, E, or F</b> (uppercase). Grade must be a single letter. Marks range from 0 to 100. The system stores both independently so you can set your own grading scale."
    },
    "file": {
        "keywords": ["file", "save", "storage", "txt", "students.txt"],
        "answer": "All records are saved in <code>students.txt</code> in the same folder as <code>app.py</code>. Each line is: <code>id,name,age,grade,marks</code>. You can open it in any text editor to inspect or back up data."
    },
    "hello": {
        "keywords": ["hi", "hello", "hey", "help", "start", "how"],
        "answer": "👋 Hello! I'm the <b>Smart SMS Assistant</b>. I can answer questions about using this app. Try asking: <i>How do I add a student?</i> or <i>Where are my analytics?</i>"
    }
}

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower().strip()
    for key, val in CHAT_RESPONSES.items():
        if any(kw in msg for kw in val["keywords"]):
            return jsonify({"reply": val["answer"]})
    return jsonify({"reply": "I'm not sure about that. Try asking: <i>How do I add a student?</i>, <i>How do I search?</i>, or <i>What does analytics show?</i>"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)