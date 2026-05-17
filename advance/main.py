import socket

HOST = '127.0.0.1'
PORT = 50432

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_socket:
        serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_socket.bind((HOST, PORT))
        serv_socket.listen()
        server_running = True
        while server_running:
            print('Ожидаю соединения')
            sock, addr = serv_socket.accept()
            with sock:
                print('Подключение по адресу:', addr)
                while True:
                    try:
                        data = sock.recv(1024)
                        if not data:
                            print(f'Клиент {addr} корректно отключился')
                            break
                        decoded_data = data.decode('utf-8')
                        print(f'Получено: "{decoded_data}", от {addr}')
                        if decoded_data.strip() == 'stop server':
                            print(f'Выключение сервера по команде от {addr}')
                            response = 'Сервер выключается.\n'
                            sock.sendall(response.encode('utf-8'))
                            server_running = False
                            break
                        data = data.upper()
                        print(f'Отправлено: {data}, по адресу: {addr}')
                        sock.sendall(data)
                    except ConnectionResetError:
                        print(f'Клиент {addr} неожиданно разорвал соединение')
                        break
                    except BrokenPipeError:
                        print(f'Клиент {addr} разорвал соединение при отправке')
                        break
                    except ConnectionError as e:
                        print(f'Ошибка соединения с {addr}: {e}')
                        break
        print('Отключение пользователя')
    print("Сервер завершает работу...")
    # Не до конца понял, нужно ли писать это вручную, это сообщение и так выводится в конце, но сделал раз было в условии
    print('Process finished with exit code 0')