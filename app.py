import tkinter as tk
from tkinter import messagebox
import sqlite3

# ----------------- Database Setup -----------------

def connect():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS book (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        year INTEGER,
        isbn TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert(title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book (title, author, year, isbn) VALUES (?, ?, ?, ?)",
                (title, author, year, isbn))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?",
                (title, author, year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("""
    UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?
    """, (title, author, year, isbn, id))
    conn.commit()
    conn.close()

# ----------------- UI Setup -----------------

def get_selected_row(event):
    try:
        global selected_tuple
        index = listbox.curselection()[0]
        selected_tuple = listbox.get(index)
        
        entry_title.delete(0, tk.END)
        entry_title.insert(tk.END, selected_tuple[1])
        
        entry_author.delete(0, tk.END)
        entry_author.insert(tk.END, selected_tuple[2])
        
        entry_year.delete(0, tk.END)
        entry_year.insert(tk.END, selected_tuple[3])
        
        entry_isbn.delete(0, tk.END)
        entry_isbn.insert(tk.END, selected_tuple[4])
    except IndexError:
        pass

def view_command():
    listbox.delete(0, tk.END)
    for row in view():
        listbox.insert(tk.END, row)

def search_command():
    listbox.delete(0, tk.END)
    for row in search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()):
        listbox.insert(tk.END, row)

def add_command():
    if title_text.get() == "" or author_text.get() == "":
        messagebox.showwarning("Input Error", "Title and Author are required fields!")
        return
    insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get()))
    clear_entries()
    view_command()

def delete_command():
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
        delete(selected_tuple[0])
        view_command()

def update_command():
    update(selected_tuple[0], title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    view_command()

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_isbn.delete(0, tk.END)

# ----------------- Main Window -----------------

connect()
window = tk.Tk()
window.title("📚 Book Management System")

# Labels
tk.Label(window, text="Title").grid(row=0, column=0, padx=10, pady=5)
tk.Label(window, text="Author").grid(row=0, column=2, padx=10, pady=5)
tk.Label(window, text="Year").grid(row=1, column=0, padx=10, pady=5)
tk.Label(window, text="ISBN").grid(row=1, column=2, padx=10, pady=5)

# Entries
title_text = tk.StringVar()
entry_title = tk.Entry(window, textvariable=title_text)
entry_title.grid(row=0, column=1)

author_text = tk.StringVar()
entry_author = tk.Entry(window, textvariable=author_text)
entry_author.grid(row=0, column=3)

year_text = tk.StringVar()
entry_year = tk.Entry(window, textvariable=year_text)
entry_year.grid(row=1, column=1)

isbn_text = tk.StringVar()
entry_isbn = tk.Entry(window, textvariable=isbn_text)
entry_isbn.grid(row=1, column=3)

# Listbox and Scrollbar
listbox = tk.Listbox(window, height=12, width=50)
listbox.grid(row=2, column=0, rowspan=6, columnspan=2, pady=10, padx=10)

scrollbar = tk.Scrollbar(window)
scrollbar.grid(row=2, column=2, rowspan=6, sticky='ns')

listbox.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=listbox.yview)

listbox.bind('<<ListboxSelect>>', get_selected_row)

# Buttons
tk.Button(window, text="View All", width=15, command=view_command).grid(row=2, column=3)
tk.Button(window, text="Search Book", width=15, command=search_command).grid(row=3, column=3)
tk.Button(window, text="Add Book", width=15, command=add_command).grid(row=4, column=3)
tk.Button(window, text="Update Selected", width=15, command=update_command).grid(row=5, column=3)
tk.Button(window, text="Delete Selected", width=15, command=delete_command).grid(row=6, column=3)
tk.Button(window, text="Clear Fields", width=15, command=clear_entries).grid(row=7, column=3)
tk.Button(window, text="Close", width=15, command=window.destroy).grid(row=8, column=3, pady=5)

window.mainloop()
