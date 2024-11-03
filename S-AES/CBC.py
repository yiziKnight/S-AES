import random
from S_AES_tools import *

# 生成16未的初始向量IV
def generate_iv():
    return [random.randint(0,1) for _ in range(16)]

# 对两个二进制列表进行异或操作
def xor(a,b):
    return [x^y for x,y in zip(a,b)]

# 使用CBC模式加密明文块
def cbc_encrypt(P,K):
    blocks = [P[i:i+16] for i in range(0,len(P),16)]
    iv = generate_iv()
    ciphertext = []

    #处理第一个块
    prev_cipher_block = iv
    for block in blocks:
        # 对块进行填充
        if len(block) < 16:
            block += [0]*(16 - len(block))

        # 对当前块进行异或操作
        xor_block = xor(block,prev_cipher_block)
        cipher_block = S_AES(xor_block,K) # 加密
        ciphertext.extend(cipher_block)
        prev_cipher_block = cipher_block # 更新前一个密文块

    return iv,ciphertext # 返回IV和密文

# 使用CBC模式解密密文
def cbc_decrypt(C,K,iv):
    blocks = [C[i:i + 16] for i in range(0, len(C), 16)]
    P = []

    # 处理第一个块
    prev_cipher_block = iv
    for block in blocks:
        decyrpted_block = Inv_S_AES(block,K)
        # 进行异或
        plain_block = xor(decyrpted_block,prev_cipher_block)
        P.extend(plain_block)
        prev_cipher_block = block

    return P

# 测试CBC模式
key = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0]
plaintext = [1, 0, 1, 0,  1, 1, 0, 0,  0, 1, 1, 1,  0, 0, 1, 1] * 4

# 加密
iv, ciphertext = cbc_encrypt(plaintext,key)
print(f"初始向量（IV）：{iv}")
print(f"加密后的密文：{ciphertext}")

# 解密
decrypted_plaintext = cbc_decrypt(ciphertext,key,iv)
print(f"解密后的明文：{decrypted_plaintext}")

# 进行密文篡改：篡改第一个密文块
modified_ciphertext = ciphertext.copy()
modified_ciphertext[0] ^= 1

# 尝试解密篡改后的密文
decrypted_modified_plaintext = cbc_decrypt(modified_ciphertext,key,iv)
print(f"解密篡改后的明文：{decrypted_modified_plaintext}")