import socket
import config
import indicator
import pickle
import asyncio

async def handle_client(client_socket, client_addr):
    print(f"Client connected: {client_addr}")
    passwd = await asyncio.to_thread(client_socket.recv, 1024)
    if passwd.decode()[0:-1] == config.PASSWORD.decode():
        if passwd.decode()[-1] == '|':
            dicti = indicator.dict_indi()
            await asyncio.to_thread(client_socket.send, pickle.dumps(dicti))
            await asyncio.to_thread(client_socket.close)
        elif passwd.decode()[-1] == '&':
            net = indicator.get_network()
            print(net)
            await asyncio.to_thread(client_socket.send, pickle.dumps(net))
            await asyncio.to_thread(client_socket.close)
        else:
            dicti = indicator.dict_data()
            await asyncio.to_thread(client_socket.send, pickle.dumps(dicti))
            await asyncio.to_thread(client_socket.close)
    else:
        await asyncio.to_thread(client_socket.send, pickle.dumps("wrong pass"))
        await asyncio.to_thread(client_socket.close)

async def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((config.IP, config.PORT))
    print(config.IP, config.PASSWORD, config.PORT)
    sock.listen(10)
    print("Server start!")
    while True:
        client_socket, client_addr = await asyncio.to_thread(sock.accept)
        asyncio.create_task(handle_client(client_socket, client_addr))

asyncio.run(main())
