import modle.des

des = modle.des.DES('data\\pc-1.csv', 'data\\pc-2.csv', 'data\\number of left shifts.csv',
                    'data\\bit selection.csv', 'data\\sbox', 'data\\P.csv',
                    'data\\IP.csv', 'data\\RIP.csv')
data = '0123456789ABCDEF'
key = '0001001100110100010101110111100110011011101111001101111111110001'
cipher = des.encrypt(data, key)
print(des.key_status())
print(cipher == '85E813540F0AB405')
