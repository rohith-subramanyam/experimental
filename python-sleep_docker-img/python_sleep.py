import datetime
import time

def main():
    while True:
        print("All I do is check time and sleep")
        print("The time now is %s" % datetime.datetime.now())
        print("Ok, I am going back to sleep now")

        time.sleep(2)

if __name__ == '__main__':
    main()
