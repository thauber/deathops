import threading

ctx = threading.local()

def clear():
    ctx.__dict__.clear()
