import socket

HOST = "127.0.0.1"
PORT = 50400


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        while True:
            print('Введите ваше сообщение или exit для выхода с сервера или stop server для остановки работы сервера.')
            data_to_send = input(': ').strip().lower()
            if data_to_send == 'exit':
                sock.close()
                print(f'Отключение от сервера')
                break
            elif data_to_send == '':
                print('Вы ввели пустую строку!')
                continue
            data_bytes_to_send = data_to_send.encode()
            sock.sendall(data_bytes_to_send)
            data_bytes_received = sock.recv(1024)
            data_received = data_bytes_received.decode()
            print(f'Получено:', data_received)
except ConnectionRefusedError:
    print('Ошибка: Сервер не запущен или недоступен')
except Exception as e:
    print(e)
# Не до конца понял, нужно ли писать это вручную, это сообщение и так выводится в конце, но сделал раз было в условии
print('Process finished with exit code 0')