import random, string, pyperclip, os, csv
import tkinter as tk
from tkinter import messagebox

password_history = []

if not os.path.isfile('words.txt'):
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon",
             "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "uva", "watermelon"]
    with open('words.txt', 'w') as file:
        file.write('\n'.join(words))
else:
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file]

def generate_custom_password(length, include_special, include_numbers, generate_phrases, user_phrase=None):
    if generate_phrases:
        if user_phrase:
            password = user_phrase
            remaining_length = length - len(user_phrase)
            chars = string.ascii_letters
            if include_special:
                chars += string.punctuation
            if include_numbers:
                chars += string.digits
            password += ''.join(random.choice(chars) for _ in range(remaining_length))
        else:
            password = ''.join(random.choice(words) for _ in range(length))
    else:
        chars = string.ascii_letters
        if include_special:
            chars += string.punctuation
        if include_numbers:
            chars += string.digits

        if user_phrase and len(user_phrase) <= length:
            remaining_length = length - len(user_phrase)
            password = ''.join(random.choice(chars) for _ in range(remaining_length))
            position = random.randint(0, remaining_length)
            password = password[:position] + user_phrase + password[position:]
        else:
            password = ''.join(random.choice(chars) for _ in range(length))
    return password

def enable_disable_options():
    phrases_enabled = phrases_var.get() == 1
    special_checkbox.config(state="normal" if not phrases_enabled else "disabled")
    numbers_checkbox.config(state="normal" if not phrases_enabled else "disabled")
    length_slider.config(state="normal" if not phrases_enabled else "disabled")
    user_phrase_entry.config(state="normal" if not phrases_enabled else "disabled")

def generate_password():
    length = length_slider.get()
    include_special = special_var.get() == 1
    include_numbers = numbers_var.get() == 1
    generate_phrases = phrases_var.get() == 1

    user_phrase = user_phrase_entry.get()
    if user_phrase and len(user_phrase) >= length:
        user_phrase = user_phrase[:length]
    
    password = generate_custom_password(length, include_special, include_numbers, generate_phrases, user_phrase)
    
    password_history.insert(0, password)
    
    if len(password_history) > 5:
        password_history.pop()
    
    result.set(password)

def copy_to_clipboard():
    password = result.get()
    pyperclip.copy(password)

def show_password_history():
    history = "\n".join(password_history)
    messagebox.showinfo("Password History", history)

def export_passwords():
    if not password_history:
        messagebox.showwarning("Export Warning", "There are no passwords to export.")
        return

    file_path = "exported_passwords.csv"
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Generated Passwords"])
        writer.writerows([[password] for password in password_history])
    messagebox.showinfo("Export Complete", "Passwords have been exported to 'exported_passwords.csv'.")

def calculate_password_strength(password):
    score = 0
    length = len(password)

    if length >= 8:
        score += 3
    elif length >= 6:
        score += 2
    else:
        score += 1

    special_characters = set(string.punctuation)
    if any(char in special_characters for char in password):
        score += 2

    if any(char.isdigit() for char in password):
        score += 2

    if any(char.isupper() for char in password) and any(char.islower() for char in password):
        score += 2

    character_variety = len(set(password))
    if character_variety >= 10:
        score += 3
    elif character_variety >= 7:
        score += 2
    elif character_variety >= 5:
        score += 1

    return score

def update_strength_label_color(score):
    if score >= 8:
        strength_label.config(fg="#0a6b22")
    elif score >= 5:
        strength_label.config(fg="#82410c")
    else:
        strength_label.config(fg="#700a20")

def update_password_strength():
    password = result.get()
    strength = calculate_password_strength(password)
    strength_label.config(text=f"Password Strength: {strength}/10")
    update_strength_label_color(strength)


screen = tk.Tk()
screen.title("Custom Password Generator")
screen.configure(bg="#e6d1ae")

screen.columnconfigure(0, weight=1)
screen.rowconfigure(0, weight=1)

frame = tk.Frame(screen)
frame.pack(padx=10, pady=10)
frame.configure(bg="#e6d1ae")

generate_button = tk.Button(frame, text="Generate Password", command=lambda: [generate_password(), update_password_strength()], bg="#5abf64", activebackground="#61d46d")
copy_button = tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard, bg="#c7547a", activebackground="#db5a85")
history_button = tk.Button(frame, text="Password History", command=show_password_history, bg="#c94242", activebackground="#e64c4c")
export_button = tk.Button(frame, text="Export Passwords", command=export_passwords, bg="#3e73d6", activebackground="#4c81e6")

result = tk.StringVar()
result_entry = tk.Entry(frame, textvariable=result, width=30)
result_entry.config(state='readonly')

length_slider = tk.Scale(frame, from_=8, to=20, orient="horizontal", label="Password Length", background="#e0bd3f", activebackground="#edc947")

special_var = tk.IntVar()
numbers_var = tk.IntVar()
phrases_var = tk.IntVar()

special_checkbox = tk.Checkbutton(frame, text="Include Special Characters", variable=special_var, bg="#e6d1ae", activebackground="#e6d1ae")
numbers_checkbox = tk.Checkbutton(frame, text="Include Numbers", variable=numbers_var, bg="#e6d1ae", activebackground="#e6d1ae")
phrases_checkbox = tk.Checkbutton(frame, text="Generate Phrases Password", variable=phrases_var, command=enable_disable_options, bg="#e6d1ae", activebackground="#e6d1ae")

user_phrase_label = tk.Label(frame, text="User Phrase:", bg="#e6d1ae")
user_phrase_entry = tk.Entry(frame, width=30)

strength_label = tk.Label(frame, text="Password Strength: 0/10", bg="#e6d1ae")

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=1)

generate_button.grid(row=0, column=0, padx=5, pady=5)
copy_button.grid(row=1, column=0, padx=5, pady=5)
history_button.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
result_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
frame.grid_rowconfigure(2, weight=1)
length_slider.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
special_checkbox.grid(row=4, column=0, padx=5, pady=5)
numbers_checkbox.grid(row=4, column=1, padx=5, pady=5)
phrases_checkbox.grid(row=4, column=2, padx=5, pady=5)
user_phrase_label.grid(row=6, column=0, padx=5, pady=5)
user_phrase_entry.grid(row=6, column=1, columnspan=2, padx=5, pady=5)
export_button.grid(row=7, column=0, padx=5, pady=5)
strength_label.grid(row=7, column=1, columnspan=2, padx=5, pady=5)

enable_disable_options()

screen.mainloop()