import struct

# Запись данных в бинарный файл
file_path = 'data_of_box.bin'

data_to_write1 = struct.pack('BBBB', 12, 23, 34, 45)
data_to_write2 = struct.pack('BBBB', 192, 168, 0, 10)

with open(file_path, 'wb') as file:
    # мусор
    file.write(b'\x00' * 10)

    # запись серийника
    file.write(data_to_write1)

    # мусор
    file.write(b'\x00' * 6)

    # запись айпи
    file.write(data_to_write2)

    # мусор
    file.write(b'\x00' * (50 - 24))


# Дешифрование данных из файла
with open(file_path, 'rb') as file:
    # дешифровка серийника
    file.seek(10)
    data1 = file.read(4)
    decoded_data1 = struct.unpack('BBBB', data1)
    value1 = ' '.join(map(str, decoded_data1))

    # дешифровка айпи
    file.seek(20)
    data2 = file.read(4)
    decoded_data2 = struct.unpack('BBBB', data2)
    value2 = '.'.join(map(str, decoded_data2))

ipipi = value2
