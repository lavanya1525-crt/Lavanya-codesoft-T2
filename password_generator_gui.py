import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import random
import string
import os # For checking image path

# --- Password Generation Logic (from previous examples) ---
def generate_password(length):
    """Generates a password of a given length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    if not characters: # Should not happen with the above
        return "Error: Char pool empty!"
    if length <= 0:
        return "Error: Length must be > 0"
    
    password_list = random.choices(characters, k=length)
    return "".join(password_list)

# --- GUI Functions ---
def on_generate_click():
    """Handles the button click event to generate and display the password."""
    try:
        length_str = length_entry.get()
        if not length_str:
            messagebox.showerror("Input Error", "Please enter a password length.")
            return

        length = int(length_str)
        if length <= 0:
            messagebox.showerror("Input Error", "Password length must be a positive number.")
            return
        if length > 128: # Optional: set a reasonable upper limit
            messagebox.showwarning("Input Warning", "Password length is very long. Consider a shorter, strong password.")
            # Or just proceed: pass

        new_password = generate_password(length)
        password_display_var.set(new_password)
        copy_button.config(state=tk.NORMAL) # Enable copy button

    except ValueError:
        messagebox.showerror("Input Error", "Invalid input. Please enter a number for length.")
        password_display_var.set("") # Clear previous password on error
        copy_button.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        password_display_var.set("")
        copy_button.config(state=tk.DISABLED)

def copy_to_clipboard():
    """Copies the generated password to the clipboard."""
    password = password_display_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        # Optional: give feedback
        # messagebox.showinfo("Copied", "Password copied to clipboard!")
        # Or change button text temporarily
        original_text = copy_button.cget("text")
        copy_button.config(text="Copied!", state=tk.DISABLED)
        root.after(1500, lambda: copy_button.config(text=original_text, state=tk.NORMAL if password_display_var.get() else tk.DISABLED))


# --- Main Application Window ---
root = tk.Tk()
root.title("Password Generator")
root.geometry("650x480+370+140") # Width x Height + X_offset + Y_offset (approx from image)
root.configure(bg="#F0F0F0") # A light background color
# root.resizable(False, False) # Optional: To make window non-resizable

# --- Style (optional, for more modern look if desired with ttk) ---
# style = ttk.Style()
# style.configure("TButton", font=("Arial", 12), padding=5)
# style.configure("TLabel", font=("Arial", 12), padding=5)
# style.configure("TEntry", font=("Arial", 12), padding=5)

# --- UI Elements ---

# 1. Top Title Label
title_label = tk.Label(root, text="PASSWORD GENERATOR SOFTWARE", font=("Times New Roman", 20, "bold"), fg="#D32F2F", bg="#F0F0F0") # Reddish color
title_label.pack(pady=(15, 10)) # Padding top and bottom

# 2. Banner Image (Placeholder - Replace with your image)
# Create an 'images' folder in the same directory as your script and put 'banner.png' there
image_path = os.path.join(os.path.dirname(__file__), "images", "banner.png") # Assumes images folder
try:
    if os.path.exists(image_path):
        banner_img = PhotoImage(file=image_path)
        # To make image responsive, you might need to resize it or use a canvas
        # For simplicity, ensure your image is roughly the right size.
        # To get closer to the image: shrink the image width a bit or allow window to be wider
        # Resizing example: banner_img = banner_img.subsample(2, 2) # Makes image 1/2 size
        image_label = tk.Label(root, image=banner_img, bg="#F0F0F0")
        image_label.image = banner_img # Keep a reference to avoid garbage collection
        image_label.pack(pady=5)
    else:
        placeholder_banner = tk.Label(root, text="[Your Banner Image Here (e.g., banner.png)]",
                                      font=("Arial", 10, "italic"), bg="lightblue",
                                      width=60, height=4, relief="solid", borderwidth=1)
        placeholder_banner.pack(pady=10)
except tk.TclError as e:
    print(f"Image Error: {e}. Check if 'images/banner.png' exists or if an image library like Pillow is needed for your image format.")
    placeholder_banner = tk.Label(root, text="[Image could not be loaded]",
                                  font=("Arial", 10, "italic"), bg="lightcoral",
                                  width=60, height=4, relief="solid", borderwidth=1)
    placeholder_banner.pack(pady=10)


# 3. Input Frame for Length
input_frame = tk.Frame(root, bg="#F0F0F0")
input_frame.pack(pady=15)

length_label_text = tk.Label(input_frame, text="Enter Password Length:", font=("Times New Roman", 14, "bold"), bg="#F0F0F0", fg="#333333") # Dark grey text
length_label_text.pack(side=tk.LEFT, padx=(0,10))

length_entry = tk.Entry(input_frame, width=10, font=("Times New Roman", 14), relief="solid", borderwidth=1)
length_entry.pack(side=tk.LEFT)
length_entry.focus_set() # Set initial focus to this entry

# 4. Generate Button
generate_button = tk.Button(root, text="GENERATE PASSWORD",
                            font=("Arial", 13, "bold"),
                            bg="#4CAF50", fg="white", # Green background, white text
                            activebackground="#45a049", activeforeground="white",
                            relief="raised", borderwidth=2,
                            width=25, height=1, # Height in text lines
                            command=on_generate_click)
generate_button.pack(pady=10)

# 5. Output Display Label (Static)
output_static_label = tk.Label(root, text="Random Password Generator:", font=("Times New Roman", 14, "bold"), bg="#F0F0F0", fg="#333333")
output_static_label.pack(pady=(10, 2))

# 6. Password Display Area (Dynamic)
password_display_var = tk.StringVar()
password_display_field = tk.Label(root, textvariable=password_display_var,
                                   font=("Courier New", 16, "bold"), # Monospaced for passwords
                                   bg="white", fg="blue",
                                   relief="sunken", borderwidth=2,
                                   width=35, # Adjust width as needed
                                   wraplength=380) # Wrap text if too long
password_display_field.pack(pady=(0, 10), ipady=5) # Internal padding

# 7. Copy to Clipboard Button
copy_button = tk.Button(root, text="Copy Password",
                        font=("Arial", 10),
                        bg="#007BFF", fg="white",
                        activebackground="#0056b3", activeforeground="white",
                        relief="raised", borderwidth=1,
                        state=tk.DISABLED, # Initially disabled
                        command=copy_to_clipboard)
copy_button.pack(pady=(0,15))


# 8. Footer Label
footer_label = tk.Label(root, text="STAY HOME STAY SAFE", font=("Arial", 10, "italic"), fg="#D32F2F", bg="#F0F0F0")
footer_label.pack(side=tk.BOTTOM, pady=(0, 10))

# --- Start the GUI Event Loop ---
root.mainloop()