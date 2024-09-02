import tkinter as tk
from tkinter import filedialog, messagebox
import firebase_admin
from firebase_admin import credentials, db, storage
import subprocess
from dotenv import load_dotenv
import os
import sys
import cv2
import numpy as np
import pandas as pd
load_dotenv()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
})

ref = db.reference('Students')
bucket = storage.bucket()

def open_main_py():
    try:
        p = sys.executable
        subprocess.run([p, "EncodeGenerator.py"], check=True)
        subprocess.run([p, "main.py"], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open main.py: {e}")

def open_add_student_form():
    def submit_form():
        name = name_entry.get()
        branch = branch_entry.get()
        roll_no = roll_no_entry.get()
        photo_path = photo_label.cget("text")
        
        if photo_path == "No file selected":
            messagebox.showwarning("Warning", "Please upload a photo.")
            return
        
        # Save student data to Firebase
        student_data = {
            "name": name,
            "major": branch,
            "starting_year": 2023,
            "total_attendance": 0,
            "standing": "G",
            "year": 1,
            "last_attendance_time": "2024-04-14 01:10:34"
        }
        ref.child(roll_no).set(student_data)

        # Save photo in ./images folder
        if not os.path.exists('./Images'):
            os.makedirs('./Images')
        img = cv2.imread(photo_path)
        resized_img = cv2.resize(img, (216, 216))
        cv2.imwrite(f'./Images/{roll_no}.png', resized_img)

        blob = bucket.blob(f'Images/{roll_no}.png')
        blob.upload_from_filename(f'./Images/{roll_no}.png')

        # Addding the new student in Attendance sheet
        df = pd.read_csv('attendance.csv')
        new_row = pd.DataFrame({col: [np.nan] for col in df.columns})
        new_row['Roll No.'] = roll_no
        new_row['Name'] = student_data["name"]
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("attendance.csv")

        messagebox.showinfo("Success", "Student data and photo added successfully!")
        add_student_window.destroy()

    add_student_window = tk.Toplevel(root)
    add_student_window.title("Add Student")

    tk.Label(add_student_window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(add_student_window, text="Branch:").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(add_student_window, text="Roll No.:").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(add_student_window, text="Photo:").grid(row=3, column=0, padx=10, pady=10)

    name_entry = tk.Entry(add_student_window)
    branch_entry = tk.Entry(add_student_window)
    roll_no_entry = tk.Entry(add_student_window)
    photo_label = tk.Label(add_student_window, text="No file selected")

    name_entry.grid(row=0, column=1, padx=10, pady=10)
    branch_entry.grid(row=1, column=1, padx=10, pady=10)
    roll_no_entry.grid(row=2, column=1, padx=10, pady=10)
    photo_label.grid(row=3, column=1, padx=10, pady=10)

    def upload_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if file_path:
            photo_label.config(text=file_path)

    tk.Button(add_student_window, text="Upload Photo", command=upload_photo).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(add_student_window, text="Submit", command=submit_form).grid(row=5, column=0, columnspan=2, pady=10)

def delete_student():
    def submit_delete():
        roll_no = roll_no_entry.get()
        
        if not roll_no:
            messagebox.showwarning("Warning", "Roll No. cannot be empty.")
            return

        # Delete local image file
        local_image_path = f'./Images/{roll_no}.png'
        if os.path.exists(local_image_path):
            os.remove(local_image_path)
        
        # Delete image from Firebase Storage
        blob = bucket.blob(f'Images/{roll_no}.png')
        if blob.exists():
            blob.delete()
        
        # Delete student record from Firebase Database
        ref.child(roll_no).delete()

        # Delete student record from Attendace sheet
        if os.path.exists('attendance.csv'):
            df = pd.read_csv('attendance.csv')
            if 'Roll No.' in df.columns:
                df['Roll No.'] = df["Roll No."].astype(str)
                df = df[df['Roll No.'] != str(roll_no)]
                df.to_csv('attendance.csv', index=False)
        
        messagebox.showinfo("Success", "Student removed from School database!")
        delete_student_window.destroy()

    delete_student_window = tk.Toplevel(root)
    delete_student_window.title("Delete Student")

    tk.Label(delete_student_window, text="Roll No.:").grid(row=0, column=0, padx=10, pady=10)
    
    roll_no_entry = tk.Entry(delete_student_window)
    roll_no_entry.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Button(delete_student_window, text="Submit", command=submit_delete).grid(row=1, column=0, columnspan=2, pady=10)



def look_attendance():
    try:
        os.startfile('attendance.csv')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open attendance.csv: {e}")

# GUI DESIGN SECTION USING TKITER

root = tk.Tk()
root.title("Attendance System")
heading_label = tk.Label(
    root, 
    text="CONTACTLESS ATTENDANCE SYSTEM", 
    font=("Arial", 24, "bold"), 
    fg="red", 
)
heading_label.pack(padx=20, pady=20, fill=tk.X)

capture_icon = tk.PhotoImage(file="Resources/capture_icon.png")
add_student_icon = tk.PhotoImage(file="Resources/add_student_icon.png")
delete_student_icon = tk.PhotoImage(file="Resources/delete_student.png")
attendance_icon = tk.PhotoImage(file="Resources/attendance_icon.png")

icon_row_frame_1 = tk.Frame(root)
icon_row_frame_1.pack(padx=20, pady=10, fill="x")

capture_frame = tk.Frame(icon_row_frame_1)
capture_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
capture_label = tk.Label(capture_frame, image=capture_icon, cursor="hand2")
capture_label.pack()
tk.Label(capture_frame, text="Detect Faces", font=("Arial", 14)).pack()
capture_label.bind("<Button-1>", lambda e: open_main_py())

add_student_frame = tk.Frame(icon_row_frame_1)
add_student_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
add_student_label = tk.Label(add_student_frame, image=add_student_icon, cursor="hand2")
add_student_label.pack()
tk.Label(add_student_frame, text="Add Student", font=("Arial", 14)).pack()
add_student_label.bind("<Button-1>", lambda e: open_add_student_form())

icon_row_frame_1.grid_columnconfigure(0, weight=1)
icon_row_frame_1.grid_columnconfigure(1, weight=1)

icon_row_frame_2 = tk.Frame(root)
icon_row_frame_2.pack(padx=20, pady=10, fill="x")

delete_student_frame = tk.Frame(icon_row_frame_2)
delete_student_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
delete_student_label = tk.Label(delete_student_frame, image=delete_student_icon, cursor="hand2")
delete_student_label.pack()
tk.Label(delete_student_frame, text="Delete Student", font=("Arial", 14)).pack()
delete_student_label.bind("<Button-1>", lambda e: delete_student())

attendance_frame = tk.Frame(icon_row_frame_2)
attendance_frame.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
attendance_label = tk.Label(attendance_frame, image=attendance_icon, cursor="hand2")
attendance_label.pack()
tk.Label(attendance_frame, text="Attendance Sheet", font=("Arial", 14)).pack()
attendance_label.bind("<Button-1>", lambda e: look_attendance())

icon_row_frame_2.grid_columnconfigure(0, weight=1)
icon_row_frame_2.grid_columnconfigure(1, weight=1)

root.mainloop()