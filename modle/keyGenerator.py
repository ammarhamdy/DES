from array import array
from collections import deque
import csv


class KeyGenerator:
    def __init__(self, pc1_csv_path: str, pc2_csv_path: str, shifts_csv_path: str):
        # load pc-1 matrix.
        self.pc1 = list(csv.reader(open(pc1_csv_path)))
        # load pc-2 matrix.
        self.pc2 = list(csv.reader(open(pc2_csv_path)))
        # load number of shifts.
        self.number_of_shifts = list(csv.reader(open(shifts_csv_path)))
        # is passed parity check.
        self.passed_parity_check: bool = True

    def sub_keys_of(self, key):
        blocks: list = [None, None, None, None, None, None, None, None]
        for i in range(8):
            # store blocks
            blocks[i] = array('u', key[8 * i:8 * (i + 1)])
            # parity check.
            self.passed_parity_check &= blocks[i].count('1') % 2 == 1
            # remove last bit.
            blocks[i].pop()
        # apply pc-1.
        c0 = d0 = str()
        for i in range(4):
            # full c0.
            for j in self.pc1[i]:
                ij = int(j) - 1
                c0 += blocks[ij // 8][ij % 8]
            # full d0.
            for k in self.pc1[i + 4]:
                ik = int(k) - 1
                d0 += blocks[ik // 8][ik % 8]
        # generate cs and ds
        c0, d0 = deque(c0, maxlen=28), deque(d0, maxlen=28)
        key_s: list = list(range(16))
        rows, columns = len(self.pc2), len(self.pc2[0])
        for n in range(16):
            c0.rotate(-1 * int(self.number_of_shifts[0][n]))
            d0.rotate(-1 * int(self.number_of_shifts[0][n]))
            sub_key, cn_dn = '', ''.join(c0) + ''.join(d0)
            # apply pc2.
            for i in range(rows):
                for j in range(columns):
                    sub_key += cn_dn[int(self.pc2[i][j]) - 1]
            key_s[n] = sub_key
        return key_s

    def is_strong_key(self):
        return self.passed_parity_check


if __name__ == '__main__':
    # keyGenerator = KeyGenerator('..\\data\\pc-1.csv', '..\\data\\pc-2.csv', '..\\data\\number of left shifts.csv')
    # keys = keyGenerator.sub_keys_of('0001001100110100010101110111100110011011101111001101111111110001')
    # for itk in keys:
    #     print(itk)
    # print('strong key:', keyGenerator.is_strong_key())
    pass
