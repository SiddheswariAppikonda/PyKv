import requests

API_URL = "http://127.0.0.1:8000"


def print_response(response):
    print("Status Code:", response.status_code)
    try:
        print("Response:", response.json())
    except:
        print("Raw Response:", response.text)


def set_value():
    key = input("Enter key: ")
    value = input("Enter value: ")

    payload = {"key": key, "value": value}
    response = requests.post(f"{API_URL}/set", json=payload)
    print_response(response)

def get_value():
    key = input("Enter key: ")
    response = requests.get(f"{API_URL}/get/{key}")
    print_response(response)


def delete_value():
    key = input("Enter key: ")
    response = requests.delete(f"{API_URL}/delete/{key}")
    print_response(response)


def get_all():
    response = requests.get(f"{API_URL}/all")
    if response.status_code == 200:
        data = response.json()
        print("\n--- Full Store ---")
        for k, v in data.get("full_store", {}).items():
            print(f"{k}: {v}")

        print("\n--- Current LRU Cache Keys ---")
        for k in data.get("current_cache", []):
            print(k)
    else:
        print_response(response)


def menu():
    while True:
        print("\n---- PyKV Client ----")
        print("1. SET")
        print("2. GET")
        print("3. DELETE")
        print("4. GET ALL")
        print("5. EXIT")

        choice = input("Choose option: ")

        if choice == "1":
            set_value()
        elif choice == "2":
            get_value()
        elif choice == "3":
            delete_value()
        elif choice == "4":
            get_all()
        elif choice == "5":
            print("Exiting client...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
