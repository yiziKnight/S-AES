import numpy as np


P = [0,1,1,0, 1,1,1,1, 0,1,1,0, 1,0,1,1]
K = [1,0,1,0, 0,1,1,1, 0,0,1,1, 1,0,1,1]

# 1.Pre-round Transformation 密钥加
def initial_change(P,K):
    P = np.array(P)
    K = np.array(K)
    result = np.bitwise_xor(P,K).tolist()
    return result


def int_to_binary_list(num):
    # 将整数转换为二进制，并去掉前缀0b
    binary_str = bin(num)[2:]
    # 填充到四位
    binary_str = binary_str.zfill(4)
    # 转换为列表形式
    binary_list = [int(bit) for bit in binary_str]
    return binary_list

def binary_list_to_int(l):
    binary_string = ''.join(str(bit) for bit in l)
    return int(binary_string,2)

# S盒
S_box = [
    [0x9,0x4,0xA,0xB],
    [0xD,0x1,0x8,0x5],
    [0x6,0x2,0x0,0x3],
    [0xC,0xE,0xF,0x7]
]
# 逆S盒
INV_S_box = [
    [0xA,0x5,0x9,0xB],
    [0x1,0x7,0x8,0xF],
    [0x6,0x0,0x2,0x3],
    [0xC,0x4,0xD,0xE]
]
# 字节替换
def Sub_bytes(R):
    # 将传入矩阵按顺序分为四个部分，每部分4bits
    R00 = R[:4]
    R10 = R[4:8]
    R01 = R[8:12]
    R11 = R[12:16]
    # print(R00, R10, R01, R11)
    # 分别将每部分的前两个bit和后两个bit计算出
    R000 = (R00[0] << 1) | R00[1]
    R001 = (R00[2] << 1) | R00[3]
    R100 = (R10[0] << 1) | R10[1]
    R101 = (R10[2] << 1) | R10[3]
    R010 = (R01[0] << 1) | R01[1]
    R011 = (R01[2] << 1) | R01[3]
    R110 = (R11[0] << 1) | R11[1]
    R111 = (R11[2] << 1) | R11[3]
    # 通过S-box进行字节替换
    S00 = S_box[R000][R001]
    S10 = S_box[R100][R101]
    S01 = S_box[R010][R011]
    S11 = S_box[R110][R111]
    S00 = int_to_binary_list(S00)
    S10 = int_to_binary_list(S10)
    S01 = int_to_binary_list(S01)
    S11 = int_to_binary_list(S11)
    result = S00 + S10 + S01 + S11
    return result

# 半字节代替求逆
def Inv_Sub_bytes(R):
    # 将传入矩阵按顺序分为四个部分，每部分4bits
    R00 = R[:4]
    R10 = R[4:8]
    R01 = R[8:12]
    R11 = R[12:16]
    # print(R00, R10, R01, R11)
    # 分别将每部分的前两个bit和后两个bit计算出
    R000 = (R00[0] << 1) | R00[1]
    R001 = (R00[2] << 1) | R00[3]
    R100 = (R10[0] << 1) | R10[1]
    R101 = (R10[2] << 1) | R10[3]
    R010 = (R01[0] << 1) | R01[1]
    R011 = (R01[2] << 1) | R01[3]
    R110 = (R11[0] << 1) | R11[1]
    R111 = (R11[2] << 1) | R11[3]
    # 通过S-box进行字节替换
    S00 = INV_S_box[R000][R001]
    S10 = INV_S_box[R100][R101]
    S01 = INV_S_box[R010][R011]
    S11 = INV_S_box[R110][R111]
    S00 = int_to_binary_list(S00)
    S10 = int_to_binary_list(S10)
    S01 = int_to_binary_list(S01)
    S11 = int_to_binary_list(S11)
    result = S00 + S10 + S01 + S11
    return result



# 行位移 ShiftRows
def ShiftRows(S):
    s1 = S[:4]
    s2 = S[4:8]
    s3 = S[8:12]
    s4 = S[12:16]
    S = s1 + s4 + s3 + s2
    return S



# 列混淆
def gf_mult(a, b):
    MOD_POLY = 0b10011
    result = 0
    while b > 0:
        # 如果 b 的最低位是1，将 a 累加到结果（异或加法）
        if b & 1:
            result ^= a
        # 左移 a，相当于乘以 x
        a <<= 1
        # 如果 a 超过4位，需要与模多项式化简
        if a & 0b10000:  # 检查 a 的第5位
            a ^= MOD_POLY
        # 右移 b，准备下一次按位乘法
        b >>= 1
    # 保证结果在4位内
    return result & 0b1111

def mix_column(S1):
    s1 = S1[:4]
    s2 = S1[4:8]
    s3 = S1[8:12]
    s4 = S1[12:16]
    s1 = binary_list_to_int(s1)
    s2 = binary_list_to_int(s2)
    s3 = binary_list_to_int(s3)
    s4 = binary_list_to_int(s4)
    s00 = s1^gf_mult(4,s2)
    s01 = s3^gf_mult(4,s4)
    s10 = s2^gf_mult(4,s1)
    s11 = s4^gf_mult(4,s3)
    s00 = int_to_binary_list(s00)
    s01 = int_to_binary_list(s01)
    s10 = int_to_binary_list(s10)
    s11 = int_to_binary_list(s11)
    s = s00 + s10 + s01 +s11
    return s

def Inv_mix_column(S1):
    s1 = S1[:4]
    s2 = S1[4:8]
    s3 = S1[8:12]
    s4 = S1[12:16]
    s1 = binary_list_to_int(s1)
    s2 = binary_list_to_int(s2)
    s3 = binary_list_to_int(s3)
    s4 = binary_list_to_int(s4)
    s00 = gf_mult(9,s1)^gf_mult(2,s2)
    s01 = gf_mult(9,s3)^gf_mult(2,s4)
    s10 = gf_mult(2,s1)^gf_mult(9,s2)
    s11 = gf_mult(2,s3)^gf_mult(9,s4)
    s00 = int_to_binary_list(s00)
    s01 = int_to_binary_list(s01)
    s10 = int_to_binary_list(s10)
    s11 = int_to_binary_list(s11)
    s = s00 + s10 + s01 +s11
    return s

# 密钥扩展
rcon1 = [1,0,0,0,0,0,0,0]
rcon2 = [0,0,1,1,0,0,0,0]



def g(temp, rcon):
    t = temp.copy()
    # 前半
    t1 = t[:2]
    t11 = (t1[0] << 1) | t1[1]
    t2 = t[2:4]
    t21 = (t2[0] << 1) | t2[1]
    # 后半
    t3 = t[4:6]
    t31 = (t3[0] << 1) | t3[1]
    t4 = t[6:8]
    t41 = (t4[0] << 1) | t4[1]

    t11 = int_to_binary_list(S_box[t11][t21]) # 前半
    t22 = int_to_binary_list(S_box[t31][t41]) # 后半
    # 经过s_box后的w1
    tt = t22+t11
    # 和论常数按位异或
    result = [a ^ b for a, b in zip(tt, rcon)]
    # 返回的是list
    return result

def key_expansion(key):
    w0 = key[:8]
    w1 = key[8:]
    w2 = [a ^ b for a, b in zip(g(w1,rcon1),w0)]
    w3 = [a ^ b for a, b in zip(w2,w1)]
    w4 = [a ^ b for a, b in zip(g(w3,rcon2),w2)]
    w5 = [a ^ b for a, b in zip(w3,w4)]
    return w2,w3,w4,w5


def S_AES(P, K):
    w2, w3, w4, w5 = key_expansion(K)
    K1 = w2 + w3
    K2 = w4 + w5
    # 1. 轮密钥加
    step1 = initial_change(P, K)

    # 第一轮加密：
    # 1. 半字节代替
    step2 = Sub_bytes(step1)

    # 2. 行位移
    step3 = ShiftRows(step2)

    # 3. 列混淆
    step4 = mix_column(step3)

    # 4. 轮密钥加
    step5 = initial_change(step4, K1)

    # 第二轮
    # 1. 半字节代替
    step6 = Sub_bytes(step5)

    # 2. 行位移
    step7 = ShiftRows(step6)

    # 3. 轮密钥加
    step8 = initial_change(step7, K2)
    return step8

def Inv_S_AES(C,K):
    w2, w3, w4, w5 = key_expansion(K)
    K1 = w2 + w3
    K2 = w4 + w5
    # 1. 轮密钥加 K2
    step1 = initial_change(C, K2)

    # 2. 行位移求逆
    step2 = ShiftRows(step1)

    # 3. 半字节代替求逆
    step3 = Inv_Sub_bytes(step2)

    # 4. 轮密钥加
    step4 = initial_change(step3, K1)

    # 5. 列混淆求逆
    step5 = Inv_mix_column(step4)

    # 6. 行位移求逆
    step6 = ShiftRows(step5)

    # 7. 半字节代替求逆
    step7 = Inv_Sub_bytes(step6)

    # 8. 轮密钥加
    step8 = initial_change(step7, K)
    return step8