# attack.py
import threading
import requests

# This URL points to your FastAPI app
# Make sure your product ID matches (likely ID 1 from your Insert statement)
API_URL = "http://127.0.0.1:8000/buy/1"

def buy_item(user_id):
    try:
        # Each thread sends a POST request
        response = requests.post(API_URL)
        print(f"User {user_id}: {response.json()['message']}")
    except Exception as e:
        print(f"User {user_id}: Connection Failed")

# We create 20 threads to simulate 20 people clicking 'Buy' instantly
threads = []
print("--- STARTING ATTACK: 20 Concurrent Users ---")

for i in range(20):
    t = threading.Thread(target=buy_item, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

print("--- ATTACK FINISHED ---")