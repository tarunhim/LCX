
import time



POLL_INTERVAL = 3 

def monitor_and_automate():

    while True:
        try:
            print("running...")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    monitor_and_automate()