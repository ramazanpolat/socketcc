# socketcc
Socket Cluster Client for Python

This is a refined fork of [https://github.com/sacOO7/socketcluster-client-python](https://github.com/sacOO7/socketcluster-client-python).

# Why fork?
The original work of [sacOO7](https://github.com/sacOO7/socketcluster-client-python) was great except the code styling.
So I refined it to conform [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/ "Style Guide for Python Code")

    
Overview
--------
This client provides following functionality

- Easy to setup and use
- Can be used for extensive unit-testing of all server side functions
- Support for emitting and listening to remote events
- Automatic reconnection
- Pub/sub
- Authentication (JWT)
- Needs python 3.6+

To install use
```python
    sudo pip install socketcc
```

Description
-----------
Create instance of `SocketCC` class by passing url of socketcluster-server end-point 

```python
    //Create a socket instance
    socket = SocketCC("ws://localhost:8000/socketcluster/") 
    
```
**Important Note** : Default url to socketcluster end-point is always *ws://somedomainname.com/socketcluster/*.

#### Registering basic listeners
 
Different functions are given as an argument to register listeners

```python
def your_code_starts_here(socket: SocketCC):
   pass

def on_connect(socket: SocketCC):
    logging.info(f"Connected to {socket.url}")

def on_disconnect(socket: SocketCC):
    logging.info(f"Disconnected from {socket.url}")

def on_connection_error(socket: SocketCC, error):
    logging.error(f"Connection error:{error}")

def on_set_auth(socket: SocketCC, token):
    logging.info(f"Received auth token:{token}")
    socket.set_auth_token(token)

def on_auth(socket: SocketCC, is_authenticated):
    logging.info("Authenticated is " + str(is_authenticated))

    def after_authenticated(eventname, error, data):
        print("token is " + json.dumps(data, sort_keys=True))
        your_code_starts_here(socket)

    socket.emit("auth", api_credentials, after_authenticated)

if __name__ == "__main__":
    scc = SocketCC(SC_ENDPOINT)
    scc.set_basic_listener(on_connect, on_disconnect, on_connection_error)
    scc.set_auth_listener(on_set_auth, on_auth)
    scc.set_reconnection(False)
    scc.connect()
```

#### Connecting to server

- For connecting to server:

```python
    //This will send websocket handshake request to socketcluster-server
    socket.connect();
```

- By default reconnection to server is enabled , to configure delay for connection

```python
    //This will set automatic-reconnection to server with delay of 2 seconds and repeating it for infinitely
    socket.setdelay(2)
    socket.connect();
```

- To disable reconnection :

```python
   socket.set_reconnection(False)
```

Emitting and listening to events
--------------------------------
#### Event emitter

- eventname is name of event and message can be String, boolean, int or JSON-object

```python

    socket.emit(eventname, message);
        
    # socket.emit("chat", "Hi")
```

- To send event with acknowledgement, provide an extra parameter for Ack callback

```python

    socket.emit("chat", "Hi", ack)  
        
    def ack(event_name, error, object):
        print "Got ack data " + object + " and error " + error + " and event_name is " + eventname
```

#### Event Listener

- For listening to events :

The object received can be String, Boolean, Long or JSONObject.

```python
     # Receiver code without sending acknowledgement back
     socket.on("ping", message)
     
     def message(eventname, object):
         print "Got data " + object + " from eventname " + eventname
```

- To send acknowledgement back to server

```python
    # Receiver code with ack
    socket.on_ack("ping", messsage_ack)
    
    def messsage_ack(eventname, object, ack_message):
        print "Got data " + object + " from eventname " + eventname
        ackmessage("this is error", "this is data")
        
```

Implementing Pub-Sub via channels
---------------------------------

#### Creating channel

- For creating and subscribing to channels:

```python
    
    # without acknowledgement
    socket.subscribe('yell')
    
    #with acknowledgement
    socket.subscribe('yell', suback)
    
    def suback(channel, error, object):
        if error is '':
            print "Subscribed successfully to channel " + channel
```

- For getting list of created channels :
 
```python
        channels = socket.channels

``` 


#### Publishing event on channel

- For publishing event :

```python

       # without acknowledgement
       socket.publish('yell', 'Hi dudies')
       
       #with acknowledgement
       socket.publish('yell', 'Hi dudies', pub_ack)
       
       def pub_ack(channel, error, object):
           if error is '':
               print "Publish sent successfully to channel " + channel
``` 
 
#### Listening to channel

- For listening to channel event :

```python
        
        socket.on_channel('yell', print_channel_message)
    
        def print_channel_message(key, object):
            print "Got data " + object + " from key " + key
    
``` 
     
#### Un-subscribing to channel

```python
         # without acknowledgement
         socket.unsubscribe('yell')
         
         # with acknowledgement
         socket.unsubscribe('yell', unsub_ack) 
         
         def unsub_ack(channel, error, object):
              if error is '':
                   print "Unsubscribed to channel " + channel 
```
      
#### Disable SSL Certificate Verification

```python
        socket = SocketCC("wss://localhost:8000/socketcluster/")
        socket.connect(sslopt={"cert_reqs": ssl.CERT_NONE})
```

#### HTTP proxy

Support websocket access via http proxy. The proxy server must allow "CONNECT" method to websocket port. Default squid setting is "ALLOWED TO CONNECT ONLY HTTPS PORT".

```python
        socket = SocketCC("wss://localhost:8000/socketcluster/")
        socket.connect(http_proxy_host="proxy_host_name", http_proxy_port=3128)
```
