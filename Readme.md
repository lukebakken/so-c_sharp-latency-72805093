Steps to reproduce

Prerequisites
- http://jagt.github.io/clumsy/index.html
- Docker
- Python
- Visual studio
- Windows

## Python Sender, C# Receiver.

1. Setup a default rabbitmq docker container. Tutorial here: https://www.architect.io/blog/2021-01-19/rabbitmq-docker-tutorial/  
  a. You only need to run the following two commands on the page: `docker pull rabbitmq:3-management`  followed by `docker run --rm -it -p 15672:15672 -p 5672:5672 rabbitmq:3-management`
2. Build the C# receiver code and run it, use the steps on this page https://www.rabbitmq.com/tutorials/tutorial-one-dotnet.html to create the vs project files
3. Run the C# receiver `dotnet run -c Release`
4. Run the python sender. You might need to install a few packages such as pika and orjson
5. The C# receivers output should print messages as it receives them, the time between each message should be ~200ms  `count: 38, TimeBetweenmessages: 00:00:00.2081190, messageSize 400060`
6. Open clumsy and set its filter as follows `outbound and ip.DstAddr >= 127.0.0.1 and ip.DstAddr <= 127.255.255.255`.  Select the Lag checkbox and its outbound checkbox and set the delay to 20ms.
7. Start Clumsy and view the output of the C# reciever as it will have jumped to a higher time between messages and fall behind. `count: 76, TimeBetweenmessages: 00:00:00.4869533, messageSize 400063` 
8. Stop the python sender, the C# client will continue to receive messages as it has fallen behind. 
9. stop the receiver.

## Python Sender, Python Receiver.
1. setup a rabbitmq docker container, see above.
2. Run the python receiver.
3. run the python sender.
4. Start clumsy with the same settings as above.
5. the latency will creep up a bit but it will still receive messages at 5hz. 
6. stop the sender and check the receiver, it will stop receiving messages as it already has them all.