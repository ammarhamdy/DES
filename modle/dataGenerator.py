import csv
import os


def xor(a: str, b: str):
    a_xor_b = str()
    for i in range(len(a)):
        a_xor_b += str(int(a[i]) ^ int(b[i]))
    return a_xor_b


class DataGenerator:
    def __init__(self, e_path: str, s_box_dir_path: str, p_path: str):
        # load bit selection matrix(8X6).
        self.e = list(csv.reader(open(e_path)))
        # load s_box directory each s-box(4X16).
        names: list = os.listdir(s_box_dir_path)
        self.s_boxes: list = \
            [list(csv.reader(open(s_box_dir_path + '\\' + names[0]))),
             list(csv.reader(open(s_box_dir_path + '\\' + names[1]))),
             list(csv.reader(open(s_box_dir_path + '\\' + names[2]))),
             list(csv.reader(open(s_box_dir_path + '\\' + names[3]))),
             list(csv.reader(open(s_box_dir_path + '\\' + names[4]))),
             list(csv.reader(open(s_box_dir_path + '\\' + names[5]))),
             list(csv.reader(open(s_box_dir_path + '\\' + names[6]))),
             list(csv.reader(open(s_box_dir_path + '\\' + names[7])))]
        # load permutation matrix(8X4).
        self.p = list(csv.reader(open(p_path)))

    def expand(self, right: str):
        """apply matrix e; from 32bits return 48bits"""
        expanded = str()
        for sub_list in self.e:
            for item in sub_list:
                expanded += right[int(item) - 1]
        return expanded

    def reduction(self, bits: str):
        """split 48bits(8*6) in to 32bit(8*4), apply SBox to each block"""
        reduction_bits = str()
        for i in range(8):
            block = bits[i * 6: (i + 1) * 6]
            reduction_bits += str(bin(int(self.s_boxes[i][int(block[0] + block[5], 2)][int(block[1:5], 2)]))[2:]) \
                .rjust(4, '0')
        return reduction_bits

    def mangler_function(self, right: str, key: str):
        """apply matrix P return 32bits"""
        r_xor_k = self.reduction(xor(self.expand(right), key))
        p_r_xor_k = str()
        for sub_list in self.p:
            for item in sub_list:
                p_r_xor_k += r_xor_k[int(item) - 1]
        return p_r_xor_k

    def round16(self, left0: str, right0: str, key_generator):
        """return data left16, right16."""
        l0, r0 = left0, right0
        for i in range(16):
            left = r0
            right = xor(l0, self.mangler_function(r0, key_generator.next_sub_key()))
            r0, l0 = right, left
        return l0, r0


if __name__ == '__main__':
    # test...
    # dataGenerator = DataGenerator('..\\data\\bit selection.csv', '..\\data\\sbox', '..\\data\\P.csv')
    # e = dataGenerator.expand('11110000101010101111000010101010')
    # print(e == '011110100001010101010101011110100001010101010101')

    # k = '000110110000001011101111111111000111000001110010'
    # r = '011110100001010101010101011110100001010101010101'
    # r_xor_k = xor(r, k)
    # print(r_xor_k == '011000010001011110111010100001100110010100100111')

    # reduction = dataGenerator.reduction_of('011000010001011110111010100001100110010100100111')
    # print(reduction == '01011100100000101011010110010111')

    # k1 = '000110110000001011101111111111000111000001110010'
    # r0 = '11110000101010101111000010101010'
    # mf = dataGenerator.mangler_function(r0, k1)
    # print(mf, '\n', mf == '00100011010010101010100110111011')

    # from keyGenerator import KeyGenerator
    # keys = KeyGenerator('..\\data\\pc-1.csv', '..\\data\\pc-2.csv', '..\\data\\number of left shifts.csv').\
    #     sub_keys_of('0001001100110100010101110111100110011011101111001101111111110001')
    # M = '0123456789ABCDEF'
    # r0 = '11110000101010101111000010101010'
    # l0 = '11001100000000001100110011111111'
    # l16r16 = dataGenerator.round16_of(l0, r0, keys)
    # print(l16r16[0] == '01000011010000100011001000110100',
    #       '\n', l16r16[1] == '00001010010011001101100110010101')
    pass
