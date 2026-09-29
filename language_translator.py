import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import MyMemoryTranslator
import threading


# Language names and codes
languages = {
    "English": "en-GB",
    "Hindi": "hi-IN",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "German": "de-DE",
    "Japanese": "ja-JP",
    "Chinese": "zh-CN",
    "Arabic": "ar-SA",
    "Russian": "ru-RU",
    "Bengali": "bn-IN",
    "Urdu": "ur-PK",
    "Portuguese": "pt-PT",
    "Italian": "it-IT"
}


# Function to translate text
def translate_text():

    text = input_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "Please enter some text!"
        )
        return

    source_name = source_language.get()
    target_name = target_language.get()

    if not source_name or not target_name:
        messagebox.showwarning(
            "Warning",
            "Please select both languages!"
        )
        return

    source = languages[source_name]
    target = languages[target_name]

    if source == target:
        messagebox.showwarning(
            "Warning",
            "Source and target languages cannot be the same!"
        )
        return

    # Disable button while translating
    translate_button.config(state="disabled")
    status_label.config(text="Translating... Please wait")

    # Clear previous output
    output_text.delete("1.0", tk.END)

    # Start translation in background
    thread = threading.Thread(
        target=perform_translation,
        args=(text, source, target),
        daemon=True
    )

    thread.start()


# Function to perform translation
def perform_translation(text, source, target):

    try:
        translator = MyMemoryTranslator(
            source=source,
            target=target
        )

        result = translator.translate(text)

        if not result:
            raise ValueError("No translation received.")

        # Update GUI from main thread
        root.after(0, show_result, result)

    except Exception as error:
        root.after(0, show_error, str(error))


# Display translated text
def show_result(result):

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

    status_label.config(
        text="Translation completed successfully!"
    )

    translate_button.config(state="normal")


# Display error message
def show_error(error):

    translate_button.config(state="normal")
    status_label.config(text="Translation failed")

    error_lower = error.lower()

    if "429" in error_lower or "too many requests" in error_lower:
        message = (
            "Too many translation requests.\n\n"
            "Please wait and try again later."
        )

    elif "connection" in error_lower or "timeout" in error_lower:
        message = (
            "Unable to connect to the translation service.\n\n"
            "Please check your internet connection."
        )

    else:
        message = (
            "Unable to translate text.\n\n"
            + error
        )

    messagebox.showerror(
        "Translation Error",
        message
    )


# Function to copy translated text
def copy_text():

    text = output_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "Warning",
            "There is no translated text to copy!"
        )
        return

    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

    status_label.config(text="Text copied successfully!")

    messagebox.showinfo(
        "Success",
        "Translated text copied successfully!"
    )


# Function to clear text
def clear_text():

    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

    status_label.config(
        text="Ready to translate"
    )


# Main window
root = tk.Tk()

root.title("Language Translator")
root.geometry("650x650")
root.resizable(False, False)
root.configure(bg="#f0f2f5")


# Heading
heading = tk.Label(
    root,
    text="Language Translator",
    font=("Arial", 24, "bold"),
    bg="#f0f2f5",
    fg="#1a237e"
)
heading.pack(pady=20)


# Language selection frame
language_frame = tk.Frame(
    root,
    bg="#f0f2f5"
)
language_frame.pack(pady=10)


# Source language
tk.Label(
    language_frame,
    text="From:",
    font=("Arial", 12, "bold"),
    bg="#f0f2f5"
).grid(row=0, column=0, padx=10)


source_language = ttk.Combobox(
    language_frame,
    values=list(languages.keys()),
    state="readonly",
    width=18
)

source_language.set("English")
source_language.grid(row=0, column=1, padx=10)


# Target language
tk.Label(
    language_frame,
    text="To:",
    font=("Arial", 12, "bold"),
    bg="#f0f2f5"
).grid(row=0, column=2, padx=10)


target_language = ttk.Combobox(
    language_frame,
    values=list(languages.keys()),
    state="readonly",
    width=18
)

target_language.set("Hindi")
target_language.grid(row=0, column=3, padx=10)


# Input label
tk.Label(
    root,
    text="Enter Text:",
    font=("Arial", 13, "bold"),
    bg="#f0f2f5"
).pack(anchor="w", padx=35, pady=10)


# Input text box
input_text = tk.Text(
    root,
    height=7,
    width=65,
    font=("Arial", 12),
    wrap="word",
    relief="solid",
    bd=1
)

input_text.pack(padx=30, pady=5)


# Translate button
translate_button = tk.Button(
    root,
    text="Translate",
    font=("Arial", 12, "bold"),
    bg="#198754",
    fg="white",
    activebackground="#146c43",
    activeforeground="white",
    width=18,
    command=translate_text
)

translate_button.pack(pady=15)


# Output label
tk.Label(
    root,
    text="Translated Text:",
    font=("Arial", 13, "bold"),
    bg="#f0f2f5"
).pack(anchor="w", padx=35, pady=10)


# Output text box
output_text = tk.Text(
    root,
    height=7,
    width=65,
    font=("Arial", 12),
    wrap="word",
    relief="solid",
    bd=1
)

output_text.pack(padx=30, pady=5)


# Button frame
button_frame = tk.Frame(
    root,
    bg="#f0f2f5"
)

button_frame.pack(pady=15)


# Copy button
copy_button = tk.Button(
    button_frame,
    text="Copy Translation",
    font=("Arial", 11, "bold"),
    bg="#0d6efd",
    fg="white",
    width=18,
    command=copy_text
)

copy_button.grid(row=0, column=0, padx=10)


# Clear button
clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Arial", 11, "bold"),
    bg="#dc3545",
    fg="white",
    width=12,
    command=clear_text
)

clear_button.grid(row=0, column=1, padx=10)


# Status label
status_label = tk.Label(
    root,
    text="Ready to translate",
    font=("Arial", 10),
    bg="#f0f2f5",
    fg="#555555"
)

status_label.pack(pady=5)


# Run application
root.mainloop()