# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import SessionLocal, create_student, get_student, get_students, update_student, delete_student

app = FastAPI()

class StudentCreate(BaseModel):
    name: str
    age: int

class StudentResponse(BaseModel):
    id: int
    name: str
    age: int

@app.post("/students/", response_model=StudentResponse)
def create_student_api(student: StudentCreate):
    db = SessionLocal()
    db_student = create_student(db, Student(name=student.name, age=student.age))
    return db_student

@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int):
    db = SessionLocal()
    db_student = get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.get("/students/", response_model=list[StudentResponse])
def read_students(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    return get_students(db, skip=skip, limit=limit)

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student_api(student_id: int, new_data: StudentCreate):
    db = SessionLocal()
    db_student = get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = new_data.dict(exclude_unset=True)
    return update_student(db, student_id, update_data)

@app.delete("/students/{student_id}", response_model=StudentResponse)
def delete_student_api(student_id: int):
    db = SessionLocal()
    db_student = get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    delete_student(db, student_id)
    return db_student

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
