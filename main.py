import time
# import requests
import hashlib
import hmac

# Seconds
TICK_INTERVAL = 60

# Api key from bittrex
API_KEY = '10b5d58a665b4b86b44b05e54b276ad3'
API_SECRET_KEY = b'63a7b7ae598c40689e23d07f1a7e6e80'

def main():
    print('Starting trader bot, ticking every ' + str(TICK_INTERVAL) + ' seconds')

    while True:
        start = time.time()
        tick()
        end = time.time()

        # Sleep the thread if needed
        if end - start <TICK_INTERVAL:
            time.sleep(TICK_INTERVAL - (end - start))

def tick():
    pass

def format_float(f):
    return "%.8" % f

if __name__ == "__main__":
    main()
