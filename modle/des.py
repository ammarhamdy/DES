from .dataGenerator import DataGenerator
from .keyGenerator import KeyGenerator
from .permutation import Permutation


class DES:
    def __init__(self, pc1_csv_path: str, pc2_csv_path: str, shifts_csv_path: str,
                 e_csv_path: str, s_box_dir_path: str, p_csv_path: str,
                 ip_path: str, rip_path: str):
        self.dataGenerator = DataGenerator(e_csv_path, s_box_dir_path, p_csv_path)
        self.keyGenerator = KeyGenerator(pc1_csv_path, pc2_csv_path, shifts_csv_path)
        self.permutation = Permutation(ip_path, rip_path)

    def encrypt(self, data: str, key: str):
        keys = self.keyGenerator.sub_keys_of(key)
        # convert key from hex to binary.
        bin_data = str()
        for i in data:
            bin_data += str(bin(int(i, 16))[2:]).rjust(4, '0')
        # apply initial permutation.
        bin_data = self.permutation.initial_permutation_of(bin_data)
        l0 = bin_data[0:32]
        r0 = bin_data[32:]
        # get data after 16 round.
        l16r16: tuple = self.dataGenerator.round16_of(l0, r0, keys)
        # swap.
        bin_data = ''.join(l16r16[1]) + ''.join(l16r16[0])
        # apply revers initial permutation.
        cipher: str = self.permutation.revers_initial_permutation_of(bin_data)
        # convert cipher from binary to hex.
        hex_cipher = str()
        for i in range(len(cipher) // 4):
            hex_cipher += hex(int(cipher[i * 4: (i + 1) * 4], 2))[2:]
        return hex_cipher.upper()

    def key_status(self):
        return 'strong key'*self.keyGenerator.is_strong_key() + 'week key'*(not self.keyGenerator.is_strong_key())


if __name__ == '__main__':
    # test...
    # des = DES('..\\data\\pc-1.csv', '..\\data\\pc-2.csv', '..\\data\\number of left shifts.csv',
    #           '..\\data\\bit selection.csv', '..\\data\\sbox', '..\\data\\P.csv',
    #           '..\\data\\IP.csv', '..\\data\\RIP.csv')
    # data1 = '0123456789ABCDEF'
    # key1 = '0001001100110100010101110111100110011011101111001101111111110001'
    # cipher1 = des.encrypt(data1, key1)
    # print(cipher1 == '85E813540F0AB405')

    # data = '0123456789ABCDEF'
    # pare_data = str()
    # for i in data:
    #     pare_data += str(bin(int(i, 16))[2:]).rjust(4, '0')
    # print(pare_data)
    # print(pare_data == '0000000100100011010001010110011110001001101010111100110111101111')
    # print(bin(5), int('1', 2))

    # bina = '1000010111101000000100110101010000001111000010101011010000000101'
    # hexa = ''
    # # print(len(bina)//4)
    # for i in range(len(bina)//4):
    #     # print(int(bin(int(bina[i*4:(i+1)*4], 2))[2:], 2))
    #     # print(hex(int(bina[i*4:(i+1)*4], 16))[2:])
    #     hexa += hex(int(bin(int(bina[i*4:(i+1)*4], 2))[2:], 2))[2:]
    # print(hexa, hexa == '85E813540F0AB405'.lower())
    pass