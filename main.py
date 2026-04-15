import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import os

# ======================
#  THEMES
# ======================
LIGHT = {"bg": "#f5f7fb", "fg": "#111827", "btn": "#4f46e5"}
DARK = {"bg": "#0f172a", "fg": "#f8fafc", "btn": "#6366f1"}

current_theme = DARK

# ======================
#  ENCRYPTION LOGIC
# ======================
def shift(text, key, enc=True):
    result = ""
    for c in text:
        if enc:
            result += chr((ord(c) + key) % 256)
        else:
            result += chr((ord(c) - key) % 256)
    return result

def xor(text, key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result

def encrypt(text, key):
    k = sum(ord(x) for x in key) % 256
    step1 = shift(text, k, True)
    step2 = step1[::-1]
    return xor(step2, key)

def decrypt(text, key):
    k = sum(ord(x) for x in key) % 256
    step1 = xor(text, key)
    step2 = step1[::-1]
    return shift(step2, k, False)

# ======================
#  TEXT FUNCTIONS
# ======================
def encrypt_text():
    text = input_box.get("1.0", tk.END).strip()
    key = key_entry.get()

    if not text or not key:
        messagebox.showerror("Error", "Enter text & key")
        return

    result = encrypt(text, key)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

def decrypt_text():
    text = input_box.get("1.0", tk.END).strip()
    key = key_entry.get()

    if not text or not key:
        messagebox.showerror("Error", "Enter text & key")
        return

    result = decrypt(text, key)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

# ======================
#  FILE FUNCTION
# ======================
def load_file():
    file = filedialog.askopenfilename()
    key = key_entry.get()
    mode = mode_var.get()

    if not file or not key:
        messagebox.showerror("Error", "Select file & enter key")
        return

    try:
        if mode == "Encrypt":
            with open(file, "rb") as f:
                data = f.read()

            ext = os.path.splitext(file)[1]

            # Convert binary to base64 (safe)
            encoded = base64.b64encode(data).decode("utf-8")

            combined = ext + "||" + encoded

            encrypted = encrypt(combined, key)

            #  make encrypted safe
            safe_encrypted = base64.b64encode(encrypted.encode("latin1")).decode("utf-8")

            save_path = file + ".enc"

            with open(save_path, "w") as f:
                f.write(safe_encrypted)

            messagebox.showinfo("Success", f"Encrypted:\n{save_path}")

        else:
            with open(file, "r") as f:
                safe_data = f.read()

            # decode safely
            encrypted_data = base64.b64decode(safe_data.encode("utf-8")).decode("latin1")

            decrypted = decrypt(encrypted_data, key)

            if "||" not in decrypted:
                messagebox.showerror("Error", "Wrong key or corrupted file")
                return

            ext, encoded = decrypted.split("||", 1)

            decoded = base64.b64decode(encoded.encode("utf-8"))

            save_path = file.replace(".enc", "_decrypted" + ext)

            with open(save_path, "wb") as f:
                f.write(decoded)

            messagebox.showinfo("Success", f"Decrypted:\n{save_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ======================
# SAVE OUTPUT
# ======================
def save_output():
    data = output_box.get("1.0", tk.END).strip()

    if not data:
        messagebox.showerror("Error", "No output to save")
        return

    file = filedialog.asksaveasfilename(defaultextension=".txt")

    if file:
        with open(file, "w") as f:
            f.write(data)

        messagebox.showinfo("Saved", "File saved successfully")

# ======================
#  CLEAR
# ======================
def clear_all():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    key_entry.delete(0, tk.END)

# ........GUI........
# ======================

root = tk.Tk()
root.title("Custom Encryption Tool")
root.geometry("800x700")
root.configure(bg="#0b1220")  # deep dark professional background

# ===== COLORS =====
BG = "#0b1220"
CARD = "#111a2e"
TEXT = "#e5e7eb"
ACCENT = "#6366f1"
SUCCESS = "#22c55e"
DANGER = "#ef4444"

# ===== TITLE =====
title = tk.Label(
    root,
    text="Custom Encryption Tool",
    font=("Helvetica", 20, "bold"),
    bg=BG,
    fg=ACCENT
)
title.pack(pady=15)

# ===== INPUT FRAME (CARD STYLE) =====
input_frame = tk.Frame(root, bg=CARD, padx=15, pady=15)
input_frame.pack(pady=10, fill="x", padx=20)

tk.Label(input_frame, text="Input Text", bg=CARD, fg=TEXT).pack(anchor="w")
input_box = tk.Text(input_frame, height=5, bg="#0f172a", fg=TEXT, insertbackground=TEXT)
input_box.pack(fill="x", pady=5)

tk.Label(input_frame, text="Secret Key", bg=CARD, fg=TEXT).pack(anchor="w", pady=(10, 0))
key_entry = tk.Entry(input_frame, show="*", bg="#0f172a", fg=TEXT, insertbackground=TEXT)
key_entry.pack(fill="x", pady=5)

# ===== MODE =====
mode_var = tk.StringVar(value="Encrypt")

mode_frame = tk.Frame(root, bg=BG)
mode_frame.pack(pady=10)

tk.Label(mode_frame, text="Mode Selection", bg=BG, fg=TEXT).pack()

tk.Radiobutton(mode_frame, text="Encrypt File", variable=mode_var, value="Encrypt",
               bg=BG, fg=TEXT, selectcolor=BG).pack(side="left", padx=10)

tk.Radiobutton(mode_frame, text="Decrypt File", variable=mode_var, value="Decrypt",
               bg=BG, fg=TEXT, selectcolor=BG).pack(side="left", padx=10)

# ===== BUTTONS =====
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)

def style_btn(text, color, cmd):
    return tk.Button(
        btn_frame,
        text=text,
        command=cmd,
        bg=color,
        fg="white",
        activebackground="#1f2937",
        width=18,
        height=2,
        relief="flat",
        cursor="hand2"
    )

style_btn("Encrypt Text", ACCENT, encrypt_text).grid(row=0, column=0, padx=5, pady=5)
style_btn("Decrypt Text", "#8b5cf6", decrypt_text).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    root,
    text="Load File (Encrypt/Decrypt)",
    command=load_file,
    bg=SUCCESS,
    fg="white",
    relief="flat",
    height=2,
    cursor="hand2"
).pack(pady=10, fill="x", padx=50)

# ===== OUTPUT =====
output_frame = tk.Frame(root, bg=CARD, padx=15, pady=15)
output_frame.pack(pady=10, fill="x", padx=20)

tk.Label(output_frame, text="Output", bg=CARD, fg=TEXT).pack(anchor="w")

output_box = tk.Text(output_frame, height=5, bg="#0f172a", fg=TEXT, insertbackground=TEXT)
output_box.pack(fill="x", pady=5)

# ===== ACTION BUTTONS =====
action_frame = tk.Frame(root, bg=BG)
action_frame.pack(pady=10)

tk.Button(
    action_frame,
    text="Save Output",
    command=save_output,
    bg=ACCENT,
    fg="white",
    relief="flat",
    width=18,
    cursor="hand2"
).grid(row=0, column=0, padx=5)

tk.Button(
    action_frame,
    text="🧹 Clear All",
    command=clear_all,
    bg=DANGER,
    fg="white",
    relief="flat",
    width=18,
    cursor="hand2"
).grid(row=0, column=1, padx=5)

root.mainloop()