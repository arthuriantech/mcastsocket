# mcastsocket
A simple example of socket wrapper to use low-level UDP multicasting

Usage
-----
```python
from mcastsocket import MulticastSocket

# The 239.0.0.0/8 range is assigned for private use
addr = ('239.10.0.1', 8000)
sock = MulticastSocket(addr)

sock.sendto(addr, b'Hello')
print(sock.receive(256))

```
This code can work in "many-to-many" mode: each process call the bind() with the same group address. Just open two shell and experiment with this.
