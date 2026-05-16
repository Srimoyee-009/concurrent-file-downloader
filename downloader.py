import requests
import threading
import time
import os
import logging

from urls import image_url_list

if not os.path.exists("Downloads"):
    os.mkdir("Downloads")

logging.basicConfig(
    filename="download.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def download(url, name):
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            file_path = os.path.join("Downloads", name)
            with open(file_path, "wb") as file:
                                file.write(response.content)
            print(f"Downloaded {name}")
            logging.info(f"SUCCESS: {name}")
            break
        except Exception as e:
            print(f"Retrying {name}...")
            logging.error(f"FAILED: {name} - {e}")

start = time.time()

for i in range(len(image_url_list)):
    download(image_url_list[i], f"{i+1}.png")

end = time.time()

print("Sequential Time:", end - start)

threads = []

start = time.time()

for i in range(len(image_url_list)):
    thread = threading.Thread(
        target=download,
        args=(image_url_list[i], f"{i+1}.png")
    )

    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()

print("Concurrent Time:", end - start)