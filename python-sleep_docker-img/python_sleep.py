import datetime
import time

def main():
    for _ in xrange(20):
        print "All I do is check time and sleep"
        print "The time now is %s" % datetime.datetime.now()
        print "Ok, I am going back to sleep now"

        time.sleep(2)

    # Testing log line greater that 64 KiB in containersvcmon.
    print "*"*175254

    while True:
        print "All I do is check time and sleep"
        print "The time now is %s" % datetime.datetime.now()
        print "Ok, I am going back to sleep now"

        time.sleep(2)

if __name__ == '__main__':
    main()
