#!/usr/bin/env python3
"""
Generate student IDs for privacy-focused system
"""

import random
import string
from datetime import datetime

def generate_student_id(class_code, student_number):
    """Generate a student ID based on class and number"""
    return f"{class_code}{student_number:03d}"

def generate_class_list(class_code, num_students):
    """Generate a list of student IDs for a class"""
    print(f"📚 Generating Student IDs for {class_code}")
    print("=" * 50)
    
    student_ids = []
    
    for i in range(1, num_students + 1):
        student_id = generate_student_id(class_code, i)
        student_ids.append(student_id)
        print(f"Student {i:2d}: {student_id}")
    
    print("=" * 50)
    print(f"✅ Generated {len(student_ids)} student IDs")
    
    # Save to file
    filename = f"student_ids_{class_code}_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w') as f:
        f.write(f"Student IDs for {class_code}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, student_id in enumerate(student_ids, 1):
            f.write(f"Student {i:2d}: {student_id}\n")
    
    print(f"💾 Saved to: {filename}")
    return student_ids

def generate_multiple_classes():
    """Generate student IDs for multiple classes"""
    classes = [
        ("CS101", 25),
        ("MATH202", 30),
        ("PHYS101", 20),
        ("ENG201", 35)
    ]
    
    print("🎓 Generating Student IDs for Multiple Classes")
    print("=" * 60)
    
    all_students = {}
    
    for class_code, num_students in classes:
        print(f"\n📚 Class: {class_code} ({num_students} students)")
        print("-" * 40)
        
        student_ids = generate_student_id(class_code, num_students)
        all_students[class_code] = student_ids
        
        for i, student_id in enumerate(student_ids, 1):
            print(f"  {i:2d}. {student_id}")
    
    # Save combined list
    filename = f"all_student_ids_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w') as f:
        f.write("Student IDs for All Classes\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for class_code, student_ids in all_students.items():
            f.write(f"\n📚 {class_code} ({len(student_ids)} students)\n")
            f.write("-" * 40 + "\n")
            
            for i, student_id in enumerate(student_ids, 1):
                f.write(f"{i:2d}. {student_id}\n")
    
    print(f"\n💾 Combined list saved to: {filename}")
    return all_students

def main():
    """Main function"""
    print("🆔 Student ID Generator")
    print("=" * 30)
    print("This tool generates student IDs for privacy-focused submissions")
    print()
    
    while True:
        print("Choose an option:")
        print("1. Generate IDs for a single class")
        print("2. Generate IDs for multiple classes")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            class_code = input("Enter class code (e.g., CS101): ").strip().upper()
            try:
                num_students = int(input("Enter number of students: "))
                generate_class_list(class_code, num_students)
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "2":
            generate_multiple_classes()
        
        elif choice == "3":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
        
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main() 