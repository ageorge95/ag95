import keyring

def save_password(service_name, username, password):
    try:
        keyring.set_password(service_name, username, password)
        print("Password saved successfully.")
    except Exception as e:
        print(f"Failed to save password: {e}")

def get_password(service_name, username):
    try:
        password = keyring.get_password(service_name, username)
        if password:
            print("Password retrieved successfully.")
            return password
        else:
            print("No password found for the given service and username.")
            return None
    except Exception as e:
        print(f"Failed to retrieve password: {e}")
        return None

def delete_password(service_name, username):
    try:
        keyring.delete_password(service_name, username)
        print("Password deleted successfully.")
    except Exception as e:
        print(f"Failed to delete password: {e}")

if __name__ == '__main__':
    save_password('my_service', 'my_username', 'my_password')

    print("Saved password", get_password('my_service', 'my_username'))