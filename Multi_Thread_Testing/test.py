import threading

def add(x: int, y: int) -> int:
    print(x + y)

def div(x: int, y: int) -> float:
    print(x / y)


t1 = threading.Thread(target=add, args=(10, 20))
t2 = threading.Thread(target=div, args=(10, 20))

t1.start()
t2.start()

t1.join()
t2.join()

print("finidshed")