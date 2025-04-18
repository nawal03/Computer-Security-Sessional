from BitVector import *
import time

CHAR_COUNT = 16
ROW_COUNT = 4
COL_COUNT = 4
ROUND_COUNT = 11

round_key = []

rc = (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36) 

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

def adjust_length(str):
    """
        - input  : string of a variable length
        - output : string of a CHAR_COUNT length
    """
    if len(str) >= CHAR_COUNT:
        return str[0:CHAR_COUNT]
    
    while len(str) < CHAR_COUNT:
        str += ' '

    return str

def make_matrix(str):
    """
        - input  : string of a CHAR_COUNT length
        - output : row major matrix of that string [dimension = ROW_COUNT * COL_COUNT]
    """
    mat =  [] 

    #init mat
    for i in range(0, ROW_COUNT):
        arr = []
        for j in range(0, COL_COUNT):
            arr.append(0)
        mat.append(arr)
    
    k = 0
    for i in range(0, ROW_COUNT):
        for j in range(0, COL_COUNT):
            mat[i][j] = ord(str[k])
            k += 1
    
    return mat

def make_transpose_matrix(mat):
    t_mat =  [] 
    #init mat
    for i in range(0, ROW_COUNT):
        arr = []
        for j in range(0, COL_COUNT):
            arr.append(0)
        t_mat.append(arr)
    
    
    for i in range(0, ROW_COUNT):
        for j in range(0, COL_COUNT):
            t_mat[i][j] = mat[j][i]
    
    return t_mat

def rot_word(w, n):
    """
        - input  : a list w and a number n
        - output : list w left shifted by n
    """
    return w[n:] + w[:n]

def sub_word(w):
    """
        - input  : a list w
        - output : list w substituted using Sbox 
    """
    for i in range(0, COL_COUNT):
        w[i] = Sbox[w[i]]
    return w

def make_round_key(key):
    """
        - input : a key
        - stores the round key values in round_key
    """
    w_list = make_matrix(adjust_length(key))
    for i in range(4, 4*ROUND_COUNT):
        if i%ROW_COUNT == 0:
            tw = sub_word(rot_word(w_list[i-1],1))
            tw[0]^=rc[(i//ROW_COUNT)-1]
            nw = []
            for j in range(0, COL_COUNT):
                nw.append(w_list[i-ROW_COUNT][j]^tw[j])
            w_list.append(nw)
        elif ROW_COUNT > 6 and i%ROW_COUNT == 4:
            tw = sub_word(w_list[i-1])
            nw = []
            for j in range(0, COL_COUNT):
                nw.append(w_list[i-ROW_COUNT][j]^tw[j])
            w_list.append(nw)
        else:
            tw = w_list[i-1]
            nw = []
            for j in range(0, COL_COUNT):
                nw.append(w_list[i-ROW_COUNT][j]^tw[j])
            w_list.append(nw)

    for i in range(0, ROUND_COUNT):
        t_round_key = []
        for j in range(0,COL_COUNT):
            t_round_key.append(w_list[i*COL_COUNT+j])
        round_key.append(t_round_key)

    for i in range(0, ROUND_COUNT):
        round_key[i] = make_transpose_matrix(round_key[i])

def add_round_key(round_key_mat, state_mat):
    for i in range(0, ROW_COUNT):
        for j in range(0, COL_COUNT):
            state_mat[i][j]^=round_key_mat[i][j]
    return state_mat

def sub_bytes(state_mat):
    for i in range(0, ROW_COUNT):
        for j in range(0, COL_COUNT):
            state_mat[i][j] = Sbox[state_mat[i][j]]
    return state_mat

def shift_rows(state_mat):
    """
        - i-th row is shifted cyclically to the left by offsets of i
    """
    for i in range(0, ROW_COUNT):
        state_mat[i] = rot_word(state_mat[i],i)
    return state_mat

def mix_column(state_mat):
    AES_modulus = BitVector(bitstring='100011011')
    new_state_mat = []
    for i in range(0, ROW_COUNT):
        temp = []
        for j in range(0, COL_COUNT):
            a = 0
            for k in range(0, ROW_COUNT):
                bv1 = Mixer[i][k]
                bv2 = BitVector(intVal = state_mat[k][j])
                bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
                a^= bv3.intValue()
            temp.append(a)
        new_state_mat.append(temp)
        
    return new_state_mat
       
def get_cipher_text(text):
    text = adjust_length(text)
    state_mat = make_transpose_matrix(make_matrix(text))
    state_mat = add_round_key(round_key[0], state_mat)
    for i in range(1, ROUND_COUNT-1):
        state_mat = add_round_key(round_key[i], mix_column(shift_rows(sub_bytes(state_mat))))
    state_mat = add_round_key(round_key[ROUND_COUNT-1], shift_rows(sub_bytes(state_mat)))
    state_mat = make_transpose_matrix(state_mat)
    cipher_text = ""
    for i in range(0, ROW_COUNT):
        for j in range(0, COL_COUNT):
            cipher_text += chr(state_mat[i][j])
    return cipher_text

def inv_sub_bytes(state_mat):
    for i in range(0, ROW_COUNT):
        for j in range(0, COL_COUNT):
            state_mat[i][j] = InvSbox[state_mat[i][j]]
    return state_mat

def inv_shift_rows(state_mat):
    """
        - i-th row is shifted cyclically to the right by offsets of i
    """
    for i in range(0, ROW_COUNT):
        state_mat[i] = rot_word(state_mat[i],COL_COUNT-i)
    return state_mat

def inv_mix_column(state_mat):
    AES_modulus = BitVector(bitstring='100011011')
    new_state_mat = []
    for i in range(0, ROW_COUNT):
        temp = []
        for j in range(0, COL_COUNT):
            a = 0
            for k in range(0, ROW_COUNT):
                bv1 = InvMixer[i][k]
                bv2 = BitVector(intVal = state_mat[k][j])
                bv3 = bv1.gf_multiply_modular(bv2, AES_modulus, 8)
                a^= bv3.intValue()
            temp.append(a)
        new_state_mat.append(temp)

    return new_state_mat
  
def get_plain_text(cipher_text):
    cipher_text = adjust_length(cipher_text)
    state_mat = make_matrix(cipher_text)
    state_mat = make_transpose_matrix(state_mat)
    state_mat = add_round_key(round_key[ROUND_COUNT-1], state_mat)
    for i in range(ROUND_COUNT-2, 0, -1):
        state_mat = inv_mix_column(add_round_key(round_key[i], inv_sub_bytes(inv_shift_rows(state_mat))))
    state_mat = add_round_key(round_key[0], inv_sub_bytes(inv_shift_rows(state_mat)))
    state_mat = make_transpose_matrix(state_mat)
    plain_text = ""
    for i in range(0, ROW_COUNT):
        for j in range(0, COL_COUNT):
            plain_text += chr(state_mat[i][j])

    return plain_text

def print_summary(str1, str2):
    str2 = adjust_length(str2)
    str3=""
    for i in range(0, CHAR_COUNT):
        str3 += str(hex(ord(str2[i])))[2:]

    print(str1,":")
    print("In Plain Text : ", str2)
    print("In ASCII : ", str3)
    print()


####  start ####
# print("Input key, text : ")
# key = input()

# #key scheduling
# start_time = time.time()
# make_round_key(key)
# key_scheduling_time = time.time()-start_time

# text = input()
# while len(text) > 0:
#     tmp = text[:CHAR_COUNT]
#     text = text [CHAR_COUNT:]

#     #encryption
#     start_time = time.time()
#     cipher_text = get_cipher_text(tmp)
#     encryption_time = time.time()-start_time
    
#     #decryption
#     start_time = time.time()
#     deciphered_text = get_plain_text(cipher_text)
#     decryption_time = time.time()-start_time

#     #summary
#     print_summary("Plain Text", tmp)
#     print_summary("Key", key)
#     print_summary("Cipher Text", cipher_text)
#     print_summary("Deciphered Text", deciphered_text)

#     print("Execution time details:")
#     print("Key Scheduling : ", key_scheduling_time, " seconds")
#     print("Encryption Time : ", encryption_time, " seconds")
#     print("Decryption Time : ", decryption_time, " seconds")
#     print("\n\n")

    







