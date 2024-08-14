import time
import requests

def ping_urls():
    while True:
        try:
            requests.get("https://linkity.onrender.com")
            requests.get("http://linkity.onrender.com")
        except requests.exceptions.RequestException as e:
            print(f"Failed to ping: {e}")
        else:
            print("Successfully pinged URLs")

        # Sleep for 5 minutes
        time.sleep(300)

if __name__ == "__main__":
    ping_urls()