import tkinter as tk
from tkinter import filedialog, scrolledtext
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")


# -------- FILE UPLOAD --------
def upload_file():

    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, content)

        status_label.config(text="File uploaded successfully")


# -------- CLEAR TEXT --------
def clear_text():

    text_input.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    question_entry.delete(0, tk.END)

    status_label.config(text="Text cleared")


# -------- IMPROVED FILL IN BLANK GENERATOR --------
def generate_fill_blanks(paragraph, limit):

    doc = nlp(paragraph)

    questions = []
    answers = []
    used_questions = set()

    allowed_labels = {"PERSON", "DATE", "ORG", "GPE", "LOC"}

    for sent in doc.sents:

        sentence = sent.text.strip()

        for ent in sent.ents:

            if len(questions) >= limit:
                break

            # Only use meaningful entities
            if ent.label_ not in allowed_labels:
                continue

            blank_sentence = sentence.replace(ent.text, "_____")

            # Avoid duplicate questions
            if blank_sentence in used_questions:
                continue

            questions.append(blank_sentence)
            answers.append(ent.text)

            used_questions.add(blank_sentence)

        if len(questions) >= limit:
            break

    return questions, answers


# -------- GENERATE QUESTIONS --------
def generate_questions():

    paragraph = text_input.get("1.0", tk.END).strip()

    if paragraph == "":
        status_label.config(text="Please enter a paragraph")
        return

    try:
        limit = int(question_entry.get())
    except:
        status_label.config(text="Enter a valid number")
        return

    questions, answers = generate_fill_blanks(paragraph, limit)

    output_box.delete("1.0", tk.END)

    output_box.insert(tk.END, "Generated Questions\n\n")

    for i, q in enumerate(questions, 1):
        output_box.insert(tk.END, f"{i}. {q}\n")

    output_box.insert(tk.END, "\nAnswer Key\n\n")

    for i, ans in enumerate(answers, 1):
        output_box.insert(tk.END, f"{i}. {ans}\n")

    status_label.config(text=f"{len(questions)} questions generated successfully")


# -------- MAIN WINDOW --------
root = tk.Tk()
root.title("FillBlanks")
root.geometry("900x700")
root.configure(bg="#eef2f3")


# -------- TITLE --------
title = tk.Label(
    root,
    text="FillBlanks",
    font=("Arial", 22, "bold"),
    bg="#eef2f3",
    fg="#2c3e50"
)
title.pack(pady=15)


# -------- INPUT FRAME --------
input_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
input_frame.pack(pady=10, padx=20, fill="x")

tk.Label(
    input_frame,
    text="Enter Paragraph",
    font=("Arial", 12, "bold"),
    bg="white"
).pack(anchor="w", padx=10, pady=5)

# Paragraph Input Area (Light Blue)
text_input = scrolledtext.ScrolledText(
    input_frame,
    height=8,
    font=("Arial", 11),
    bg="#d6eaf8",
    fg="black"
)

text_input.pack(padx=10, pady=10, fill="x")


# -------- BUTTON FRAME --------
button_frame = tk.Frame(root, bg="#eef2f3")
button_frame.pack(pady=10)

upload_btn = tk.Button(
    button_frame,
    text="Upload File",
    width=15,
    bg="#3498db",
    fg="white",
    font=("Arial", 10, "bold"),
    command=upload_file
)

upload_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(
    button_frame,
    text="Clear Text",
    width=15,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 10, "bold"),
    command=clear_text
)

clear_btn.grid(row=0, column=1, padx=10)


# -------- SETTINGS FRAME --------
settings_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
settings_frame.pack(pady=10, padx=20, fill="x")

tk.Label(
    settings_frame,
    text="Number of Questions:",
    bg="white",
    font=("Arial", 11)
).grid(row=0, column=0, padx=10, pady=10)

question_entry = tk.Entry(settings_frame, width=10)
question_entry.grid(row=0, column=1)

generate_btn = tk.Button(
    settings_frame,
    text="Generate Questions",
    bg="#2ecc71",
    fg="white",
    font=("Arial", 10, "bold"),
    width=18,
    command=generate_questions
)

generate_btn.grid(row=0, column=2, padx=20)


# -------- OUTPUT FRAME --------
output_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
output_frame.pack(pady=10, padx=20, fill="both", expand=True)

tk.Label(
    output_frame,
    text="Generated Questions and Answers",
    font=("Arial", 12, "bold"),
    bg="white"
).pack(anchor="w", padx=10, pady=5)

# Output Area
output_box = scrolledtext.ScrolledText(
    output_frame,
    height=15,
    font=("Arial", 11),
    bg="#e3f2fd",
    fg="#1a237e"
)

output_box.pack(padx=10, pady=10, fill="both", expand=True)


# -------- STATUS BAR --------
status_label = tk.Label(
    root,
    text="Ready",
    bd=1,
    relief="sunken",
    anchor="w",
    bg="#d6eaf8"
)

status_label.pack(fill="x", side="bottom")


root.mainloop()
