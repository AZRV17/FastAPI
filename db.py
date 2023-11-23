# database.py
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)


Base.metadata.create_all(bind=engine)


def get_student(db, student_id):
    return db.query(Student).filter(Student.id == student_id).first()


def get_students(db, skip: int = 0, limit: int = 10):
    return db.query(Student).offset(skip).limit(limit).all()


def create_student(db, student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def update_student(db, student_id, new_data):
    db.query(Student).filter(Student.id == student_id).update(new_data)
    db.commit()
    return get_student(db, student_id)


def delete_student(db, student_id):
    student = db.query(Student).filter(Student.id == student_id).first()
    db.query(Student).filter(Student.id == student_id).delete()
    db.commit()
    return student


def main():
    while True:
        os.system('cls')
        print("\n")
        print("1. Create Student")
        print("2. Get Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("0. Exit")
        choice = input("Enter your choice: ")

        db = SessionLocal()

        if choice == "1":
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            student = create_student(db, Student(name=name, age=age))
            print(f"Student created with id: {student.id}")

        elif choice == "2":
            students = get_students(db)
            print("Students:")
            for student in students:
                print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}")

        elif choice == "3":
            student_id = int(input("Enter student id to update: "))
            new_name = input("Enter new name: ")
            new_age = int(input("Enter new age: "))
            update_data = {"name": new_name, "age": new_age}
            updated_student = update_student(db, student_id, update_data)
            print(
                f"Student updated: ID: {updated_student['id']}, Name: {updated_student['name']}, Age: {updated_student['age']}")

        elif choice == "4":
            student_id = int(input("Enter student id to delete: "))
            deleted_student = delete_student(db, student_id)
            print(
                f"Student deleted: ID: {deleted_student['id']}, Name: {deleted_student['name']}, Age: {deleted_student['age']}")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()
