import ctypes
import sys
import subprocess


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_command_as_admin(command, debug=False):
    shell32 = ctypes.windll.shell32
    if is_admin():
        subprocess.run(command, check=True)
        return True

    if debug:
        print(f'Running command as admin: {command}')

    ret = shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(command), None, 1)
    if int(ret) <= 32:
        print("Failed to run command with admin rights")
        return False
    return None


def sync_windows_time():
    command = ["w32tm", "/resync"]
    result = run_command_as_admin(command, debug=True)
    if result is None:
        print("Re-launched script with admin privileges.")
        sys.exit(0)
    print("Time synchronization complete.")


if __name__ == "__main__":
    sync_windows_time()
