# python-socket-server
Python 3.7+
## Usage
### Basic
```python
from kserver import KServer, KServerInterface

server = KServer(55555) # Listening on port 55555
kiface = KServerInterface(server)
kiface.Run()
```
### Custom Log
```python
# ...
def CustomLog(msg):
  print(f"Something just happened : {msg}")

server = KServer(55555, CustomLog)
# ...
```
### Add command
```python
# ...
kiface = KServerInterface(server)

def Send(interface, target, *args):
  # Mandatory args:
  # - interface is the KServerInterface object that will call the command
  # - target is one of the asyncio.Transport objects selected on the interface Listbox
  # - *args
  target.write((" ".join(args)).encode("utf8"))
  
kiface.commands["send"] = Send
kiface.Run()
```
### Alias example
```python
# ...
kiface.commands["helloworld"] = lambda interface, target, *args: Send(interface, target, "Hello World!")
kiface.Run()
```
