# Server side plan

## Functionality to be implemented
- Hosting connections between different clients
> i.e. client 1 and 2 connects to server. They are prompted with which client to connect with in order to have a conversation.  
> Suppose 1 wants to talk to 2. 2 is notified of this and asked to accept or reject the connection from user 1.  
> Both users accept, connection is started. 
- Basic records of the current texting session
> Future version is to only show records of currently happening text history
> This may be updated in some future update

## Functionality implementation methods
- Hosting connections
> Use networking to support connections from other devices and not just localhost  
> Support different OS (Linux, macOS) terminals to also connect to running server by another machine  
> Use multi-threading (Python method) to handle different sessions of 2 connected clients to receive and send messages