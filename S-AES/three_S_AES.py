from S_AES_tools import *

P = [0,1,1,0, 1,1,1,1, 0,1,1,0, 1,0,1,1]
K = [1,0,1,0, 0,1,1,1, 0,0,1,1, 1,0,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]

def three_S_AES(P,K):
    key1 = K[:16]
    key2 = K[16:]
    C1 = S_AES(P, key1)
    C2 = S_AES(C1, key2)
    C3 = S_AES(C2,key1)
    return C3

a = three_S_AES(P,K)
print(a)