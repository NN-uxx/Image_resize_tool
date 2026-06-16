import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# ================================
# バッチ処理本体
# ================================
def run_batch():
    input_dir = input_dir_var.get()

    if not input_dir:
        messagebox.showerror("エラー", "入力フォルダを指定してください")
        return

    try:
        resize_ratio = float(resize_var.get())
        if resize_ratio <= 0:
            raise ValueError
        if resize_ratio > 4.0:
            messagebox.showerror("エラー", "リサイズ倍率は最大 4.0 までです")
            return
    except ValueError:
        messagebox.showerror("エラー", "リサイズ倍率は 0 より大きい数値を入力してください")
        return

    output_dir = os.path.join(input_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # 入力フォルダ内の画像を処理
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue

        img_path = os.path.join(input_dir, filename)

        # 元ファイル名と拡張子を分離
        name, ext = os.path.splitext(filename)

        # R を付けた新しいファイル名
        new_filename = f"{name}R{ext}"

        out_path = os.path.join(output_dir, new_filename)

        img = Image.open(img_path)

        # RGBA も RGB もそのまま扱える
        img = img.convert("RGBA") if img.mode in ("RGBA", "LA") else img.convert("RGB")

        new_size = (
            int(img.width * resize_ratio),
            int(img.height * resize_ratio)
        )

        resized = img.resize(new_size, Image.LANCZOS)
        resized.save(out_path)

    messagebox.showinfo("完了", "リサイズ処理が完了しました！")

# ================================
# GUI
# ================================
def select_input_dir():
    path = filedialog.askdirectory()
    if path:
        input_dir_var.set(path)

root = tk.Tk()
root.title("画像リサイズツール")
root.configure(bg="#88bdbb")  # ← 好きな色に変更

input_dir_var = tk.StringVar()
resize_var = tk.StringVar(value="1.0")

tk.Label(root, text="入力フォルダ").grid(row=0, column=0, sticky="w")
tk.Entry(root, textvariable=input_dir_var, width=40).grid(row=0, column=1)
tk.Button(root, text="選択", command=select_input_dir).grid(row=0, column=2)

tk.Label(root, text="リサイズ倍率 (0.1〜4.0)").grid(row=1, column=0, sticky="w")
tk.Entry(root, textvariable=resize_var, width=10).grid(row=1, column=1, sticky="w")

tk.Button(root, text="リサイズ開始", command=run_batch, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10)

root.mainloop()
