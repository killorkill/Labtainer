#!/usr/bin/env python3

import socket
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes

# Thông tin RSA của Alice
ALICE_N = 22266616657574989868109324252160663470925207690694094953312891282341426880506924648525181014287214350136557941201445475540830225059514652125310445352175047408966028497316806142156338927162621004774769949534239479839334209147097793526879762417526445739552772039876568156469224491682030314994880247983332964121759307658270083947005466578077153185206199759569902810832114058818478518470715726064960617482910172035743003538122402440142861494899725720505181663738931151677884218457824676140190841393217857683627886497104915390385283364971133316672332846071665082777884028170668140862010444247560019193505999704028222347577
ALICE_E = 3

FLAG = "crypto{y0ur_v0t3_i5_my_v0t3}"

# Hàm xử lý khi nhận được dữ liệu vote từ client
def handle_vote(vote_hex):
    try:
        # Chuyển vote từ hex thành số nguyên
        vote = int(vote_hex, 16)
        # Giải mã vote sử dụng public key của Alice
        verified_vote = long_to_bytes(pow(vote, ALICE_E, ALICE_N))
        # Loại bỏ padding (nếu có) và lấy phần thông điệp thật
        vote_msg = verified_vote.split(b'\00')[-1]

        if vote_msg == b'VOTE FOR PEDRO':
            return json.dumps({"flag": FLAG})
        else:
            return json.dumps({"error": "You should have voted for Pedro"})
    except Exception as e:
        return json.dumps({"error": "Exception thrown", "exception": str(e)})

# Thiết lập server socket
def start_server(host='0.0.0.0', port=13375):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started at {host}:{port}")

    while True:
        # Chấp nhận kết nối từ client
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_socket.sendall(b"Place your vote. Pedro offers a reward to anyone who votes for him!\n")

        # Nhận dữ liệu từ client
        data = client_socket.recv(1024).decode('utf-8')
        try:
            # Parse dữ liệu JSON
            vote_data = json.loads(data)
            if 'option' in vote_data and vote_data['option'] == 'vote':
                response = handle_vote(vote_data['vote'])
            else:
                response = json.dumps({"error": "Invalid option"})
        except json.JSONDecodeError:
            response = json.dumps({"error": "Invalid JSON format"})

        # Gửi lại phản hồi cho client
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

if __name__ == '__main__':
    start_server()
