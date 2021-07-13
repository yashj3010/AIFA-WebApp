import schedule
import time
import test

def job():
    print("I'm working...")

schedule.every(10).seconds.do(test.job)

while True:
    schedule.run_pending()
    time.sleep(1)