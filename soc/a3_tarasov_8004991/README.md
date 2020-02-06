Requerement:
    - Python 3
1. Start server.py
2. Run client side with following commands:
    - python3 client.py test #(will run with test msg defined in lab manual)
    - python3 client.py your message #(will concatinate "your message" on empty space string and send it to the server)
    - chmod 755 will terminate the need of using python3 explicitly.
Additional:
    - Running client script with empty input will result in exit with error.
    - If length of packet not dev by 8, msg will be appended with " ".