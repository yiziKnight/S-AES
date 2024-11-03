import tkinter as tk
from tkinter import ttk
from S_AES_tools import *

# 输入验证函数
def is_valid_binary_string(input_str):
    return all(char in '01' for char in input_str)

# ASCII码转换为二进制列表
def ascii_str_to_binary_str_list(ascii_str):
    return [bin(ord(char))[2:].zfill(16) for char in ascii_str]

# 列表转换为ASCII码
def binary_str_list_to_ascii_str(binary_str_list):
    return "".join([chr(int(binary_str, 2)) for binary_str in binary_str_list])

root = tk.Tk()
root.title("S-AES加解密工具")
root.geometry("400x300")

a_frame = ttk.Frame(root)
b_frame = ttk.Frame(root)

def show_a_frame():
    b_frame.pack_forget()  # 隐藏解密框架
    a_frame.pack(fill='both', expand=True)  # 显示加密框架

def show_b_frame():
    a_frame.pack_forget()  # 隐藏加密框架
    b_frame.pack(fill='both', expand=True)  # 显示解密框架

# 顶部导航按钮
nav_frame = ttk.Frame(root)
nav_frame.pack(side="top", fill="x")

encrypt_button = ttk.Button(nav_frame, text="加密", command=show_a_frame)
encrypt_button.pack(side="left", padx=5, pady=5)

decrypt_button = ttk.Button(nav_frame, text="解密", command=show_b_frame)
decrypt_button.pack(side="left", padx=5, pady=5)

# 加密界面组件
p_label = ttk.Label(a_frame, text="请输入明文 :")
p_label.pack(pady=5)

p_entry = ttk.Entry(a_frame)
p_entry.pack(pady=5)

k_label = ttk.Label(a_frame, text="请输入密钥 :")
k_label.pack(pady=5)

k_entry = ttk.Entry(a_frame)
k_entry.pack(pady=5)

encrypt_result_label = ttk.Label(a_frame, text="加密结果:")
encrypt_result_label.pack(pady=5)

def a():
    p_str = p_entry.get()
    k_str = k_entry.get()

    if not is_valid_binary_string(k_str):
        encrypt_result_label.config(text="输入有误，请输入只包含 0 和 1 的字符串。")
        return

    # 判断明文是ASCII码还是二进制数
    is_binary_plaintext = all(char in '01' for char in p_str)
    if is_binary_plaintext:
        P = [int(char) for char in p_str]
        K = [int(char) for char in k_str]
        C = S_AES(P, K)
        encrypt_result_label.config(text=f"加密结果: {C}")
    else:
        binary_plaintext_list = ascii_str_to_binary_str_list(p_str)
        encrypted_binary_chunks = []
        for binary_chunk in binary_plaintext_list:
            P = [int(char) for char in binary_chunk]
            K = [int(char) for char in k_str]
            encrypted_chunk = S_AES(P, K)
            encrypted_binary_chunks.append("".join(map(str, encrypted_chunk)))
        ascii_str = binary_str_list_to_ascii_str(encrypted_binary_chunks)
        print(ascii_str)
        encrypt_result_label.config(text=f"加密结果：{ascii_str}")

encrypt_button = ttk.Button(a_frame, text="加密", command=a)
encrypt_button.pack(pady=10)

# 解密界面组件
c_label = ttk.Label(b_frame, text="请输入密文 :")
c_label.pack(pady=5)

c_entry = ttk.Entry(b_frame)
c_entry.pack(pady=5)

k_label_decrypt = ttk.Label(b_frame, text="请输入密钥 :")
k_label_decrypt.pack(pady=5)

k_entry_decrypt = ttk.Entry(b_frame)
k_entry_decrypt.pack(pady=5)

decrypt_result_label = ttk.Label(b_frame, text="解密结果:")
decrypt_result_label.pack(pady=5)

# 解密函数
def b():
    c_str = c_entry.get()
    k_str = k_entry_decrypt.get()

    if not is_valid_binary_string(k_str):
        decrypt_result_label.config(text="输入有误，请输入只包含 0 和 1 的字符串。")
        return

    is_binary_plaintext = all(char in '01' for char in c_str)
    if is_binary_plaintext:
        C = [int(char) for char in c_str]
        K = [int(char) for char in k_str]
        P = Inv_S_AES(C, K)
        decrypt_result_label.config(text=f"解密结果: {P}")
    else:
        binary_ciphertext_list = ascii_str_to_binary_str_list(c_str)
        decrypted_binary_chunks = []
        for binary_chunk in binary_ciphertext_list:
            C = [int(char) for char in binary_chunk]
            K = [int(char) for char in k_str]
            decrypted_chunk = Inv_S_AES(C, K)
            decrypted_binary_chunks.append("".join(map(str, decrypted_chunk)))
        decrypted_ascii_str = binary_str_list_to_ascii_str(decrypted_binary_chunks)
        decrypt_result_label.config(text=f"解密结果：{decrypted_ascii_str}")

decrypt_button = ttk.Button(b_frame, text="解密", command=b)
decrypt_button.pack(pady=10)

# 默认显示加密界面
show_a_frame()

# 运行主循环
root.mainloop()
