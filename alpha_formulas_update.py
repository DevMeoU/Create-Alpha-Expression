import tkinter as tk
from tkinter import ttk, messagebox
import os

FILE_PATH = "alpha_formulas.txt"

def load_formulas(file_path):
    """
    Đọc file và tách ra phần header và danh sách các entry.
    Mỗi entry gồm 2 dòng: dòng STATUS và dòng công thức.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    header = []
    entries = []
    i = 0
    # Lấy header cho đến khi gặp dòng bắt đầu bằng "STATUS:"
    while i < len(lines) and not lines[i].strip().startswith("STATUS:"):
        header.append(lines[i])
        i += 1
    
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("STATUS:"):
            status = "IN USE" if "IN USE" in line.split("|")[0] else "YET TO USE"
            i += 1
            if i < len(lines):
                formula = lines[i].rstrip("\n")
                i += 1
            else:
                formula = ""
            entries.append({"status": status, "formula": formula})
        else:
            i += 1
    return header, entries

def save_formulas(file_path, header, entries):
    """
    Ghi lại file theo cấu trúc ban đầu:
    - Ghi header
    - Với mỗi entry: ghi dòng STATUS mới và dòng công thức (indent 4 spaces)
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(header)
        for entry in entries:
            status_line = f"STATUS: {entry['status']}\n"
            f.write(status_line)
            f.write(f"    {entry['formula']}\n\n")

def main():
    if not os.path.exists(FILE_PATH):
        messagebox.showerror("Error", f"File {FILE_PATH} không tồn tại!")
        return

    header, entries = load_formulas(FILE_PATH)

    root = tk.Tk()
    root.title("Alpha Formula Status Editor")

    # Tạo một khung chính chứa Canvas và Scrollbar
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    status_vars = []
    # Hiển thị danh sách các công thức trong scrollable_frame
    for idx, entry in enumerate(entries):
        var = tk.IntVar(value=1 if entry['status'] == "IN USE" else 0)
        status_vars.append(var)
        chk = ttk.Checkbutton(scrollable_frame, text=entry['formula'], variable=var)
        chk.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=2)

    def on_save():
        for idx, var in enumerate(status_vars):
            entries[idx]['status'] = "IN USE" if var.get() == 1 else "YET TO USE"
        save_formulas(FILE_PATH, header, entries)
        messagebox.showinfo("Saved", "Đã cập nhật trạng thái vào file.")

    btn_save = ttk.Button(root, text="Save", command=on_save)
    btn_save.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
