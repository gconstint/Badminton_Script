import ctypes
import subprocess
import sys
import time
from datetime import datetime


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        # Support for PyInstaller wrapped program.
        arguments = map(str, argv[1:])
    else:
        arguments = map(str, argv)
    argument_line = u' '.join(arguments)
    executable = str(sys.executable)
    if debug:
        print('Command line: ', executable, argument_line)
    ret = shell32.ShellExecuteW(None, "runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None


def sync_windows_time(time_server="time.windows.com"):
    try:
        # Configure the time server
        configure_cmd = f'w32tm /config /syncfromflags:manual /manualpeerlist:"{time_server}" /update'
        subprocess.run(configure_cmd, check=True, shell=True)

        # Resync the time
        resync_cmd = 'w32tm /resync'
        subprocess.run(resync_cmd, check=True, shell=True)

        print("Time synchronization successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def execute_delay():
    if not is_admin():
        print("Requesting administrator privileges...")
        result = run_as_admin()
        if result is None:
            print("Re-launching script with admin privileges...")
            sys.exit()
        elif not result:
            print("Failed to run with admin rights - cannot sync time.")
            sys.exit()
    else:
        if len(sys.argv) > 1:
            sync_windows_time(sys.argv[1])
        else:
            now = datetime.now().strftime("%H:%M:%S")
            print("Now time:", now)
            target = datetime.strptime("11:59:00","%H:%M:%S")
            print("Target time: 11:59:00")
            s_time = abs(target - datetime.strptime(now, "%H:%M:%S"))
            s_time = int(s_time.total_seconds())
            print(f"sleeping for {s_time} seconds...")
            time.sleep(s_time)
            sync_windows_time()
    # input("Press Enter to exit...")


if __name__ == "__main__":
    execute_delay()
