import socket
import pickle
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def get_first_data(ip: str, port: int, passwd: str):
    try:
        a = b"p"
        sock = socket.socket()
        sock.connect((ip, port))
        passwd = bytes(passwd.encode()) + a
        sock.send(passwd)

        data = sock.recv(1024)
        sock.close()
        return pickle.loads(data)
    except Exception as e:
        logging.error(f"Error getting first data: {e}")
        return None


async def get_indicat(ip: str, port: int, passwd: str):
    try:
        a = b"|"
        sock = socket.socket()
        sock.connect((ip, port))
        passwd = bytes(passwd.encode()) + a
        sock.send(passwd)

        data = sock.recv(1024)
        sock.close()
        return pickle.loads(data)
    except Exception as e:
        logging.error(f"Error getting indicators value: {e}")
        return None

async def get_network_speed(ip: str, port: int, passwd : str):
    try:
        a = b"&"
        sock = socket.socket()
        sock.connect((ip, port))
        passwd = bytes(passwd.encode()) + a
        sock.send(passwd)

        data = sock.recv(1024)
        sock.close()
        return pickle.loads(data)
    except Exception as e:
        logging.error(f"Error getting network speed: {e}")
        return None
