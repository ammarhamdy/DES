from array import array
from collections import deque
import csv


def binary(hexadecimal: str):
    return ''.join([str(bin(int(i, 16))[2:]).rjust(4, '0') for i in hexadecimal])


class KeyGenerator:
    """
    1. takes key 16 bits(hex) --> 64 bits(binary).
    2. apply pc-1(8X7) return 56 bits.
    3. split key to C0, D0 28bits.
    4. rotate C0, D0 return C1, D1.
    5. C1+''+D1 = sub key1.
    6. apply pc-2(8X6) to sub key1 return 48bits.
    7. C1` = rotate(C1), D1` = rotate(D1).
    """
    def __init__(self, pc1_csv_path: str, pc2_csv_path: str, shifts_csv_path: str):
        # load pc-1 matrix(8X7).
        self.pc1 = list(csv.reader(open(pc1_csv_path)))
        # load pc-2 matrix(8X6).
        self.pc2 = list(csv.reader(open(pc2_csv_path)))
        # load number of shifts(16 value).
        self.number_of_shifts = list(csv.reader(open(shifts_csv_path)))
        # is passed parity check.
        self.passed_parity_check: bool = True
        # index of round.
        self.n = 0
        # first c, d
        self.c0 = self.d0 = deque()

    def apply_pc1(self, blocks: list):
        # 8 row, 7 column.
        # rows, columns = len(self.pc1), len(self.pc1[0])
        c0 = d0 = ''
        for i in range(4):
            # full c0 with first 4 rows.
            c0 += ''.join([blocks[(int(j)-1) // 8][(int(j)-1) % 8] for j in self.pc1[i]])
            # full d0 with second 4 rows.
            d0 += ''.join([blocks[(int(j)-1) // 8][(int(j)-1) % 8] for j in self.pc1[i+4]])
        return c0, d0

    def apply_pc2(self, cn_dn: str):
        # 8 row, 6 column.
        # rows, columns = len(self.pc2), len(self.pc2[0])
        sub_key: str = ''
        for i in range(8):
            for j in range(6):
                sub_key += cn_dn[int(self.pc2[i][j]) - 1]
        return sub_key

    def set_key(self, key: str):
        # convert key from hex to binary.
        key: str = binary(key)
        blocks: list = [None, None, None, None, None, None, None, None]
        for i in range(8):
            # store blocks
            blocks[i] = array('u', key[8 * i:8 * (i + 1)])
            # parity check.
            self.passed_parity_check &= blocks[i].count('1') % 2 == 1
            # remove last bit.
            blocks[i].pop()
        # apply pc-1.
        c, d = self.apply_pc1(blocks)
        self.c0, self.d0 = deque(c, maxlen=28), deque(d, maxlen=28)

    def next_sub_key(self):
        self.c0.rotate(-1 * int(self.number_of_shifts[0][self.n]))
        self.d0.rotate(-1 * int(self.number_of_shifts[0][self.n]))
        self.n += 1
        return self.apply_pc2(''.join(self.c0) + ''.join(self.d0))

    def is_strong_key(self):
        return self.passed_parity_check


if __name__ == '__main__':
    # test...
    # keyGenerator = KeyGenerator('..\\data\\pc-1.csv', '..\\data\\pc-2.csv', '..\\data\\number of left shifts.csv')
    # keyGenerator.set_key('133457799BBCDFF1')
    # for itk in range(16):
    #     print(keyGenerator.next())
    # print('strong key:', keyGenerator.is_strong_key())
    pass
