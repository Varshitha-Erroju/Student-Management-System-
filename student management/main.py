from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE = "students.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def calculate_grade(marks):
    marks = int(marks)
    if marks >= 90:
        return "A+"
    elif marks >= 75:
        return "B"
    elif marks >= 50:
        return "C"
    else:
        return "Fail"

@app.get("/api/students")
def get_students():
    return load_data()

@app.post("/api/students")
def add_student(student: dict):
    students = load_data()
    for s in students:
        if str(s["roll"]) == str(student["roll"]):
            raise HTTPException(status_code=400, detail="Roll exists")
    student["marks"] = int(student["marks"])
    student["grade"] = calculate_grade(student["marks"])
    students.append(student)
    save_data(students)
    return student

@app.put("/api/students/{roll}")
def update_student(roll: int, data: dict):
    students = load_data()
    for s in students:
        if str(s["roll"]) == str(roll):
            if "marks" in data and str(data["marks"]).strip() != "":
                s["marks"] = int(data["marks"])
                s["grade"] = calculate_grade(s["marks"])
            if "branch" in data and data["branch"]:
                s["branch"] = data["branch"]
            if "name" in data and data["name"]:
                s["name"] = data["name"]
            save_data(students)
            return {"message": "Updated"}
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/api/students/{roll}")
def delete_student(roll: int):
    students = load_data()
    new_list = [s for s in students if str(s["roll"]) != str(roll)]
    if len(new_list) == len(students):
        raise HTTPException(status_code=404, detail="Not found")
    save_data(new_list)
    return {"message": "Deleted"}

# IMPORTANT - Check where is index.html
if os.path.exists("frontend/index.html"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
else:
    app.mount("/", StaticFiles(directory=".", html=True), name="static")