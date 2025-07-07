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
> Multiple threads should not influence other users who are chatting

## Basic run through of how program will work
- Server is started
> Port number is given, and confirms no errors occurred
- Client 1 connects to port
> Client 1 name is requested. Save its unique "key" (selectors.selectorKey)    
> Client 1 IP and port connection from is saved
- Client 2 connects to port
> Client 2 name is requested, saved  
> Client 2 IP and port connection from is saved
- Client 1 is shown list of online users by their username and IP
> Client 1 selects which user to connect to
- CURRENT VERSION: Client 1 connects to Client 2, automatically occurs
> Client 2 is updated and their connection starts. Server creates new thread for them to communicate
- Client 1 and 2 are able to talk to each other
> Client 1 message -> server -> server sends to Client 2.  
> Same process for client 2 to 1
- Ending occurs when interrupted. 
> If 1 client ends process, the other is sent back to start page, displaying all active users

- Definitely need some sort of communication protocol, at least for accepting new users in
> Need to record their username and their connection details