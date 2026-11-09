from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE_NAME = "students.json"

def get_grade(m):
    try:
        m=int(m)
        if m>=90: return "A+"
        elif m>=75: return "B"
        elif m>=50: return "C"
        else: return "Fail"
    except:
        return "-"

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            data = json.load(open(FILE_NAME, "r"))
            # paatha data ki kuda grade add chey
            for s in data:
                if 'grade' not in s or s['grade'] == 'undefined':
                    s['grade'] = get_grade(s.get('marks',0))
            return data
        except:
            return []
    return []

def save_data(data):
    json.dump(data, open(FILE_NAME, "w"), indent=4)

@app.get("/api/students")
def get_students():
    return load_data()

@app.post("/api/students")
def add_student(student: dict):
    data = load_data()
    if any(s['roll'] == student['roll'] for s in data):
        return {"error": "Roll already exists"}
    student['grade'] = get_grade(student['marks'])
    data.append(student)
    save_data(data)
    return {"message": "Added"}

@app.delete("/api/students/{roll}")
def delete_student(roll: str):
    data = load_data()
    new_data = [s for s in data if s['roll'] != roll]
    save_data(new_data)
    return {"message": "Deleted"}

@app.put("/api/students/{roll}")
def update_student(roll: str, updated: dict):
    data = load_data()
    for s in data:
        if s['roll'] == roll:
            s['marks'] = updated['marks']
            s['grade'] = get_grade(updated['marks'])
    save_data(data)
    return {"message": "Updated"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")