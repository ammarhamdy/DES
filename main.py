import modle.des


des = modle.des.DES('data\\pc-1.csv', 'data\\pc-2.csv', 'data\\number of left shifts.csv',
                    'data\\bit selection.csv', 'data\\sbox', 'data\\P.csv',
                    'data\\IP.csv', 'data\\RIP.csv')
data = '0123456789ABCDEF'
key = '133457799BBCDFF1'
if len(data) != 16:
    print('data length error!')
    exit(0)
if len(key) != 16:
    print('key length error!')
    exit(0)
cipher = des.encrypt(data, key)
print(des.key_status())
print(cipher)
print(cipher == '85E813540F0AB405')
