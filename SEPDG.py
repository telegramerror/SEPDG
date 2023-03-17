import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as tkmessagebox
from tkinter import ttk
from itertools import product
import threading

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        self.combination_label = tk.Label(self, text="Combination Method:")
        self.combination_label.grid(row=0, column=0, sticky="w")
        self.combination_entry = tk.Entry(self)
        self.combination_entry.grid(row=0, column=1, columnspan=2, sticky="we")
        self.combination_entry.insert(0, "ABC,ACB,ACC,AB,AC")
        
        self.a_label = tk.Label(self, text="A Item:")
        self.a_label.grid(row=1, column=0, sticky="w")
        self.a_entry = tk.Text(self, height=10, width=30)
        self.a_entry.config(wrap=tk.CHAR)
        self.a_entry.grid(row=2, column=0)
        self.a_import_button = tk.Button(self, text="Import Text", command=self.import_a_file)
        self.a_import_button.grid(row=3, column=0)
        
        self.b_label = tk.Label(self, text="B Item:")
        self.b_label.grid(row=1, column=1, sticky="w")
        self.b_entry = tk.Text(self, height=10, width=30)
        self.b_entry.config(wrap=tk.CHAR)
        self.b_entry.grid(row=2, column=1)
        self.b_import_button = tk.Button(self, text="Import Text", command=self.import_b_file)
        self.b_import_button.grid(row=3, column=1)
        
        self.c_label = tk.Label(self, text="C Item:")
        self.c_label.grid(row=1, column=2, sticky="w")
        self.c_entry = tk.Text(self, height=10, width=30)
        self.c_entry.config(wrap=tk.CHAR)
        self.c_entry.grid(row=2, column=2)
        self.c_import_button = tk.Button(self, text="Import Text", command=self.import_c_file)
        self.c_import_button.grid(row=3, column=2)
        
        self.generate_button = tk.Button(self, text="Generate Dictionary", command=self.generate_dictionary)
        self.generate_button.grid(row=4, column=1)
        
        self.progress_label = tk.Label(self, text="Progress: 0%")
        self.progress_label.grid(row=5, column=1)
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress_bar.grid(row=6, column=1)
        self.link_label = tk.Label(self, text="https://t.me/cvehub", fg="blue", cursor="hand2")
        self.link_label.grid(row=7, column=2, sticky="se")
        self.link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://t.me/cvehub"))

    def import_a_file(self):
        file_path = filedialog.askopenfilename()
        with open(file_path, "r") as f:
            self.a_entry.delete(1.0, tk.END)
            self.a_entry.insert(tk.END, f.read())
            
    def import_b_file(self):
        file_path = filedialog.askopenfilename()
        with open(file_path, "r") as f:
            self.b_entry.delete(1.0, tk.END)
            self.b_entry.insert(tk.END, f.read())
    def import_c_file(self):
        file_path = filedialog.askopenfilename()
        with open(file_path, "r") as f:
            self.c_entry.delete(1.0, tk.END)
            self.c_entry.insert(tk.END, f.read())
            
    def generate_dictionary(self):
        combination_method = self.combination_entry.get().strip().replace(" ", "").split(",")
        if combination_method == [""]:
            tkmessagebox.showerror("Error", "Please enter a valid combination method.")
            return

        a_passwords = self.a_entry.get(1.0, tk.END).strip().split("\n")
        b_passwords = self.b_entry.get(1.0, tk.END).strip().split("\n")
        c_passwords = self.c_entry.get(1.0, tk.END).strip().split("\n")

        if a_passwords == [""] or b_passwords == [""] or c_passwords == [""]:
            tkmessagebox.showerror("Error", "Please enter at least one password in each item.")
            return

        combinations = set()
        for method in combination_method:
            passwords_product = []
            for char in method:
                if char == "A":
                    passwords_product.append(a_passwords)
                elif char == "B":
                    passwords_product.append(b_passwords)
                elif char == "C":
                    passwords_product.append(c_passwords)
            combinations.update(product(*passwords_product))
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as f:
                total_combinations = len(combinations)
                for i, combination in enumerate(combinations):
                    f.write("".join(combination) + "\n")
                    progress = int(((i + 1) / total_combinations) * 100)
                    self.progress_bar["value"] = progress
                    self.progress_label.config(text=f"Progress: {progress}%")
                    
    def start(self):
        self.master.mainloop()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Social Engineering Password Dictionary Generator")
    app = Application(master=root)
    app.start()
