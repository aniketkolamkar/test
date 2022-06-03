from sympy import im
import scheduler
import time

def test():
    print("Pragya")

scheduler.every(10).seconds.do(test)

while 1:
    scheduler.run_pending()
    time.sleep(1)