from S_AES_tools import *
P = [0,1,1,0, 1,1,1,1, 0,1,1,0, 1,0,1,1]
K = [1,0,1,0, 0,1,1,1, 0,0,1,1, 1,0,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]
C = [1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0]

def int_to_binary_list(num):
    # 将整数转换为二进制，并去掉前缀0b
    binary_str = bin(num)[2:]
    # 填充到十六位
    binary_str = binary_str.zfill(16)
    # 转换为列表形式
    binary_list = [int(bit) for bit in binary_str]
    return binary_list

def double_S_AES(P,K):
    key1 = K[:16]
    key2 = K[16:]
    C1 = S_AES(P,key1)
    C2 = S_AES(C1,key2)
    return C2

a = double_S_AES(P,K)
print(a)


def meet_in_middle_attack(P, C):
    middle_dict = {}
    count = 0
    # 第一部分：构建中间密文的映射
    for K1 in range(2 ** 16):  # 假设 K1 是 16 位
        K1_binary = int_to_binary_list(K1)  # 将整数转换为二进制列表
        C1 = S_AES(P, K1_binary)  # 使用 S_AES 进行加密
        middle_dict[tuple(C1)] = K1_binary  # 使用元组作为字典的键

    # 第二部分：查找可能的 K2
    for K2 in range(2 ** 16):  # 假设 K2 是 16 位
        K2_binary = int_to_binary_list(K2)  # 将整数转换为二进制列表
        C1_prime = Inv_S_AES(C, K2_binary)  # 使用逆 S_AES 进行解密

        # 检查是否找到了匹配的中间密文
        if tuple(C1_prime) in middle_dict:
            K1 = middle_dict[tuple(C1_prime)]  # 找到对应的 K1
            count +=1
            print(f"找到密钥：K1 = {K1}，K2 = {K2_binary}")
    print(count)


meet_in_middle_attack(P,C)