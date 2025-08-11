import tkinter as tk
from tkinter import messagebox, Toplevel, Label
import requests

# UI COLORS
BACKGROUND = "#fefae0"
TEXT_COLOR = "#333"
FONT = ("Segoe UI", 12)

# MEANING
def fetch_meaning():
    word = entry.get().strip()

    if word == "":
        messagebox.showwarning("Input Needed", "Please enter a word.")
        return

    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Not Found", "Word not found in dictionary.")
        return

    data = response.json()

    if len(data) == 0 or 'meanings' not in data[0]:
        messagebox.showerror("Error", "No meanings found.")
        return

    definition = data[0]['meanings'][0]['definitions'][0]['definition']
    part_of_speech = data[0]['meanings'][0]['partOfSpeech']
    example = data[0]['meanings'][0]['definitions'][0].get('example', "No example found.")

    # Display results
    result_text.config(state='normal')
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Word: {word.title()}\n", "title")
    result_text.insert(tk.END, f"Part of Speech: {part_of_speech}\n\n")
    result_text.insert(tk.END, f"Meaning: {definition}\n\n")
    result_text.insert(tk.END, f"Example: {example}")
    result_text.config(state='disabled')

# CLEAR FUNCTION
def clear_fields():
    entry.delete(0, tk.END)
    result_text.config(state='normal')
    result_text.delete(1.0, tk.END)
    result_text.config(state='disabled')

# EXIT FUNCTION
def exit_app():
    window.quit()

# ABOUT
def open_about_window():
    about = Toplevel(window)
    about.title("About")
    about.geometry("300x200")
    about.config(bg=BACKGROUND)
    about.iconbitmap(r"About.ico")

    Label(about, text="📘 Dictionary App", font=("Segoe UI", 16, "bold"), bg=BACKGROUND, fg=TEXT_COLOR).pack(pady=10)
    Label(about, text="Created by:\nVaibhav", bg=BACKGROUND, fg=TEXT_COLOR, font=FONT).pack(pady=5)
    Label(about, text="Version: 6.9\nDeveloped in Python", bg=BACKGROUND, fg=TEXT_COLOR, font=("Segoe UI", 10)).pack(pady=10)

def add_tooltip(widget, text):
    def on_enter(e):
        tooltip.place(x=e.x_root + 10, y=e.y_root + 10)
        tooltip.config(text=text)

    def on_leave(e):
        tooltip.place_forget()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

# UI
window = tk.Tk()
window.title("Dictionary App")
window.geometry("600x450")
window.config(bg=BACKGROUND)
window.iconbitmap(r"Dic.ico")

tooltip = Label(window, bg="#333", fg="white", font=("Segoe UI", 9), bd=1, relief="solid")
tooltip.place_forget()

tk.Label(window, text="Dictionary App", font=("Segoe UI", 20, "bold"),
         bg=BACKGROUND, fg=TEXT_COLOR).pack(pady=10)

entry = tk.Entry(window, font=FONT, width=30, justify="center")
entry.pack(pady=10)

# ----- 2x2 Button Grid Layout -----
btn_frame = tk.Frame(window, bg=BACKGROUND)
btn_frame.pack(pady=10)

# Configure grid weights for even spacing
btn_frame.grid_columnconfigure(0, weight=1, uniform="button")
btn_frame.grid_columnconfigure(1, weight=1, uniform="button")
btn_frame.grid_rowconfigure(0, weight=1)
btn_frame.grid_rowconfigure(1, weight=1)

# Row 0: Search and Clear buttons
search_btn = tk.Button(btn_frame, text="🔍 Search", command=fetch_meaning,
                       bg="#4CAF50", fg="white", font=FONT, padx=20, pady=5,
                       width=12)  # Green
search_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

clear_btn = tk.Button(btn_frame, text="🧹 Clear", command=clear_fields,
                      bg="#FF9800", fg="white", font=FONT, padx=20, pady=5,
                      width=12)  # Orange
clear_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Row 1: About and Exit buttons
about_btn = tk.Button(btn_frame, text="👥 About Us", command=open_about_window,
                      bg="#2196F3", fg="white", font=FONT, padx=20, pady=5,
                      width=12)  # Blue
about_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

exit_btn = tk.Button(btn_frame, text="🚪 Exit", command=exit_app,
                     bg="#F44336", fg="white", font=FONT, padx=20, pady=5,
                     width=12)  # Red
exit_btn.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
# ---------------------------------

result_text = tk.Text(window, height=12, width=65, font=FONT, wrap="word",
                      bg="white", fg=TEXT_COLOR)
result_text.tag_configure("title", font=("Segoe UI", 14, "bold"))
result_text.pack(pady=10)
result_text.config(state='disabled')


window.mainloop()
