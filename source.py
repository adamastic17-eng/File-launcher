import customtkinter as ctk
from tkinter import filedialog
import os
import json

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("900x700")
root.title("File Launcher [1.0]")

SAVE_FILE = "files.json"
files = []


# ------------------ LOAD / SAVE ------------------

def load_files():
    global files
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                files = json.load(f)
        except:
            files = []


def save_files():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(files, f, indent=4)


# ------------------ OPEN FUNCTIONS ------------------


import subprocess
import sys

def open_file(path):
    if not os.path.exists(path):
        return

    try:
        # Run python files properly
        if path.endswith(".py"):
            subprocess.run([sys.executable, path])
        else:
            os.startfile(path)

    except Exception as e:
        print("Open error:", e)


# ------------------ OPEN WITH (FIXED) ------------------

def open_with(path):
    if not os.path.exists(path):
        return

    try:
        subprocess.run([
            "rundll32.exe",
            "shell32.dll,OpenAs_RunDLL",
            path
        ])

    except Exception as e:
        print("OpenWith error:", e)

# ------------------ FILE MANAGEMENT ------------------

def add_file():
    path = filedialog.askopenfilename()

    if path and path not in files:
        files.append(path)
        save_files()
        refresh_files()


def remove_file(path):
    if path in files:
        files.remove(path)
        save_files()
        refresh_files()


# ------------------ UI ------------------

def refresh_files():
    for widget in file_frame.winfo_children():
        widget.destroy()

    for path in files:
        row = ctk.CTkFrame(file_frame, fg_color="#252525", corner_radius=12)
        row.pack(fill="x", padx=12, pady=6)

        name = os.path.basename(path)

        # Open (default)
        open_btn = ctk.CTkButton(
            row,
            text=name,
            command=lambda p=path: open_file(p),
            font=("Segoe UI", 14),
            fg_color="#333335",
            hover_color="#444446",
            anchor="w"
        )
        open_btn.pack(side="left", fill="x", expand=True, padx=6, pady=8)

        # Open With (Windows chooser)
        with_btn = ctk.CTkButton(
            row,
            text="Open With",
            width=110,
            command=lambda p=path: open_with(p),
            fg_color="#2b2b2b",
            hover_color="#4444aa"
        )
        with_btn.pack(side="right", padx=6)

        # Remove
        remove_btn = ctk.CTkButton(
            row,
            text="✕",
            width=40,
            command=lambda p=path: remove_file(p),
            fg_color="#2b2b2b",
            hover_color="#aa3333"
        )
        remove_btn.pack(side="right", padx=6)


# Title
title = ctk.CTkLabel(
    root,
    text="File Launcher",
    font=("Segoe UI", 30, "bold")
)
title.pack(pady=20)


# Add button
add_btn = ctk.CTkButton(
    root,
    text="+ Add File",
    command=add_file,
    font=("Segoe UI", 15),
    width=160,
    height=40,
    corner_radius=14,
    border_width=2,
    border_color="#aaaaaa",
    fg_color="#333335",
    hover_color="#444446"
)
add_btn.pack(pady=10)


# Scroll area
file_frame = ctk.CTkScrollableFrame(
    root,
    fg_color="#181818",
    corner_radius=18
)
file_frame.pack(fill="both", expand=True, padx=20, pady=20)


# Start
load_files()
refresh_files()

root.mainloop()
