import winreg as reg


def remove_subkeys(key):
    try:
        i = 0
        while True:
            subkey_name = reg.EnumKey(key, i)
            subkey = reg.OpenKey(key, subkey_name, 0, reg.KEY_ALL_ACCESS)
            reg.DeleteKey(subkey, "")  # Delete all subkeys
            reg.CloseKey(subkey)
            i += 1
    except WindowsError as e:
        if e.winerror != 259:  # No more data available
            print(f"An error occurred: {e}")


def remove_registry_entries():
    file_types = ['.jpg', '.jpeg', '.png',
                  '.mp4', '.mov', '.wav', '.avi', '.webp']
    keys = [
        f'SystemFileAssociations\\{file_type}\\shell\\Compress File' for file_type in file_types]

    confirmation = input(
        "This will remove certain registry entries. Are you sure? (yes/no): ")
    if confirmation.lower() != 'yes':
        print("Operation cancelled.")
        return

    for key in keys:
        try:
            reg_key = reg.OpenKey(reg.HKEY_CLASSES_ROOT,
                                  key, 0, reg.KEY_ALL_ACCESS)
            remove_subkeys(reg_key)  # Delete all subkeys
            # Now safe to delete the main key
            reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key)
            reg.CloseKey(reg_key)
        except FileNotFoundError:
            pass  # Key doesn't exist, nothing to do
        except PermissionError:
            print(f"Access denied. Unable to delete {key}.")
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    remove_registry_entries()


if __name__ == '__main__':
    main()
