from .dataGenerator import DataGenerator
from .keyGenerator import KeyGenerator
from .permutation import Permutation


def convert_to_binary(hexadecimal: str):
    return ''.join([str(bin(int(i, 16))[2:]).rjust(4, '0') for i in hexadecimal])


class DES:
    def __init__(self, pc1_csv_path: str, pc2_csv_path: str, shifts_csv_path: str,
                 e_csv_path: str, s_box_dir_path: str, p_csv_path: str,
                 ip_path: str, rip_path: str):
        self.dataGenerator = DataGenerator(e_csv_path, s_box_dir_path, p_csv_path)
        self.keyGenerator = KeyGenerator(pc1_csv_path, pc2_csv_path, shifts_csv_path)
        self.permutation = Permutation(ip_path, rip_path)

    def encrypt(self, data: str, key: str):
        # convert key from hex to binary.
        bin_key: str = convert_to_binary(key)
        # generate keys.
        keys: list = self.keyGenerator.sub_keys_of(bin_key)
        # convert data from hex to binary.
        bin_data = convert_to_binary(data)
        # apply initial permutation.
        bin_data = self.permutation.initial_permutation_of(bin_data)
        l0, r0 = bin_data[0:32], bin_data[32:]
        # get data after 16 round.
        l16r16: tuple = self.dataGenerator.round16_of(l0, r0, keys)
        # swap.
        bin_data = ''.join(l16r16[1]) + ''.join(l16r16[0])
        # apply revers initial permutation.
        cipher: str = self.permutation.revers_initial_permutation_of(bin_data)
        # convert cipher from binary to hex.
        hex_cipher = ''.join([hex(int(cipher[i * 4: (i + 1) * 4], 2))[2:] for i in range(len(cipher) // 4)])
        return hex_cipher.upper()

    def key_status(self):
        return 'strong key'*self.keyGenerator.is_strong_key() + 'week key'*(not self.keyGenerator.is_strong_key())


if __name__ == '__main__':
    # test...
    # des = DES('..\\data\\pc-1.csv', '..\\data\\pc-2.csv', '..\\data\\number of left shifts.csv',
    #           '..\\data\\bit selection.csv', '..\\data\\sbox', '..\\data\\P.csv',
    #           '..\\data\\IP.csv', '..\\data\\RIP.csv')
    # data1 = '0123456789ABCDEF'
    # key1 = '133457799BBCDFF1'
    # cipher1 = des.encrypt(data1, key1)
    # print(cipher1 == '85E813540F0AB405')

    # data = '0123456789ABCDEF'
    # pare_data = str()
    # for i in data:
    #     pare_data += str(bin(int(i, 16))[2:]).rjust(4, '0')
    # print(pare_data)
    # print(pare_data == '0000000100100011010001010110011110001001101010111100110111101111')
    # print(bin(5), int('1', 2))
    pass
