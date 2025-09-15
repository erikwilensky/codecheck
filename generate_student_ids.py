#!/usr/bin/env python3
"""
Generate student IDs for privacy-focused system
"""

import random
import string
from datetime import datetime

def generate_student_id(student_number):
    """Generate a student ID based on number"""
    return f"STU{student_number:03d}"

def generate_student_list(num_students):
    """Generate a list of student IDs"""
    print(f"📚 Generating Student IDs")
    print("=" * 50)
    
    student_ids = []
    
    for i in range(1, num_students + 1):
        student_id = generate_student_id(i)
        student_ids.append(student_id)
        print(f"Student {i:2d}: {student_id}")
    
    print("=" * 50)
    print(f"✅ Generated {len(student_ids)} student IDs")
    
    # Save to file
    filename = f"student_ids_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w') as f:
        f.write(f"Student IDs\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, student_id in enumerate(student_ids, 1):
            f.write(f"Student {i:2d}: {student_id}\n")
    
    print(f"💾 Saved to: {filename}")
    return student_ids

def generate_custom_format():
    """Generate student IDs with custom format"""
    print("🆔 Custom Student ID Generator")
    print("=" * 40)
    
    prefix = input("Enter prefix (e.g., CS, MATH, ENG): ").strip().upper()
    start_num = int(input("Enter starting number: "))
    num_students = int(input("Enter number of students: "))
    
    print(f"\n📚 Generating {num_students} student IDs with prefix '{prefix}'")
    print("=" * 50)
    
    student_ids = []
    
    for i in range(num_students):
        student_number = start_num + i
        student_id = f"{prefix}{student_number:03d}"
        student_ids.append(student_id)
        print(f"Student {i+1:2d}: {student_id}")
    
    print("=" * 50)
    print(f"✅ Generated {len(student_ids)} student IDs")
    
    # Save to file
    filename = f"student_ids_{prefix}_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w') as f:
        f.write(f"Student IDs for {prefix}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, student_id in enumerate(student_ids, 1):
            f.write(f"Student {i:2d}: {student_id}\n")
    
    print(f"💾 Saved to: {filename}")
    return student_ids

def main():
    """Main function"""
    print("🆔 Student ID Generator")
    print("=" * 30)
    print("This tool generates student IDs for privacy-focused submissions")
    print()
    
    while True:
        print("Choose an option:")
        print("1. Generate simple sequential IDs (STU001, STU002, etc.)")
        print("2. Generate custom format IDs")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            try:
                num_students = int(input("Enter number of students: "))
                generate_student_list(num_students)
            except ValueError:
                print("❌ Please enter a valid number")
        
        elif choice == "2":
            try:
                generate_custom_format()
            except ValueError:
                print("❌ Please enter valid numbers")
        
        elif choice == "3":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
        
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main() 