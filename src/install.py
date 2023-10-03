import ctypes
import os
import sys
import winreg as reg


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def add_registry_entries():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_types = ['.jpg', '.png', '.mp4', '.mov', '.wav', '.avi', '.webp']

    for file_type in file_types:
        # Set the command for the 'Compress' option
        command = f'cmd /c "{os.path.join(current_dir, "run.bat")} " "%v"'
        print(f"Adding Compress File option to {file_type}")
        registry_path = f'SystemFileAssociations\\{file_type}\\shell\\Compress File\\command'

        try:
            # Create the necessary registry keys and subkeys
            reg_key = reg.CreateKeyEx(
                reg.HKEY_CLASSES_ROOT, registry_path, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(reg_key, '', 0, reg.REG_SZ, command)
            reg.CloseKey(reg_key)
        except Exception as e:
            print(f"Failed to create registry entry for {file_type}: {e}")


def main():
    # Check if the program is running with admin rights
    if not is_admin():
        print("The script is not running with admin rights. Trying to get admin rights...")
        # Try to elevate privileges
        run_as_admin()
    else:
        # Add registry entries
        add_registry_entries()


if __name__ == '__main__':
    main()
