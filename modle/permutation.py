import csv


class Permutation:
    def __init__(self, ip_path: str, rip_path: str):
        # load initial permutation matrix.
        self.ip = list(csv.reader(open(ip_path)))
        # load revers initial permutation matrix.
        self.rip = list(csv.reader(open(rip_path)))

    def initial_permutation_of(self, data: str):
        """takes data 64bits(binary) return 64bits"""
        ip_data = str()
        for sub_list in self.ip:
            for item in sub_list:
                ip_data += data[int(item) - 1]
        return ip_data

    def revers_initial_permutation_of(self, data: str):
        """takes data 64bits(binary) return 64bits"""
        rip_data = str()
        for sub_list in self.rip:
            for item in sub_list:
                rip_data += data[int(item) - 1]
        return rip_data

    # def swap_of(self, data: str):
    #     length = len(data)//2
    #     return data[length:] + data[:length]


if __name__ == '__main__':
    # test...
    # permutation = Permutation('..\\data\\IP.csv', '..\\data\\RIP.csv')
    # m = '0000000100100011010001010110011110001001101010111100110111101111 '
    # ip = permutation.initial_permutation_of(m)
    # print(ip, '\n', ip == '1100110000000000110011001111111111110000101010101111000010101010')
    #
    # m = '0000101001001100110110011001010101000011010000100011001000110100'
    # rip = permutation.revers_initial_permutation_of(m)
    # print(rip, '\n', rip == '1000010111101000000100110101010000001111000010101011010000000101')
    #
    # m = '0100001101000010001100100011010000001010010011001101100110010101'
    # sw = permutation.swap_of(m)
    # print(sw, '\n', sw == '0000101001001100110110011001010101000011010000100011001000110100')
    pass
