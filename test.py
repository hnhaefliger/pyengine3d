with open('SharkV.txt', 'r') as f:
    a = f.readlines()
    f.close()

print(a[0])
print(a[0][:-2].split(' '))
