import socket
import threading

HOST = "127.0.0.1"
PORT = 50400

server_running = True

def handle_connection(sock, addr):
    global server_running

    with sock:
        print(f'Подключение по адресу: {addr}')
        while server_running:
            # Receive
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
                print(f'Отправлено: "{decoded_data.upper()}", по адресу: {addr}')
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




if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_socket:
        serv_socket.bind((HOST, PORT))
        serv_socket.listen()
        threads = []
        while server_running:
            try:
                if not threads:
                    print('Ожидаю соединения...')
                    serv_socket.settimeout(10)
                try:
                    sock_, addr_ = serv_socket.accept()
                    thread = threading.Thread(target=handle_connection, args=(sock_, addr_))
                    thread.daemon = True
                    thread.start()
                    threads.append(thread)
                except socket.timeout:
                    continue
            except KeyboardInterrupt:
                print('\nАктивировано принудительное прерывание')
                server_running = False
                break
        print('Сервер прекращает работу')
        for thread in threads:
            if  thread.is_alive():
                thread.join(timeout=1.0)
    # Не до конца понял, нужно ли писать это вручную, это сообщение и так выводится в конце, но сделал раз было в условии
    print('Process finished with exit code 0')