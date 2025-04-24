import sys
import os
import platform
import shutil # Use shutil.which to find the executable on PATH
import subprocess

def main():
    """
    Entry point for the 'swashes' command. Finds the C++ 'swashes'
    executable on the system PATH and replaces the current Python process
    with it using os.execl (Unix) or runs it via subprocess.call (Windows).
    """
    executable_name = "swashes"
    executable_path = shutil.which(executable_name)

    if executable_path is None:
        print(f"Error: The '{executable_name}' command was not found in the system PATH.", file=sys.stderr)
        print("Ensure the package installation was successful and the environment is activated.", file=sys.stderr)
        sys.exit(1)

    # Get arguments to pass to the executable
    # The first argument to execl should be the executable path itself
    args = [executable_path] + sys.argv[1:]

    try:
        if platform.system() == "Windows":
            # On Windows, os.execl is less common/reliable for this use case.
            # Use subprocess.call and exit with its return code.
            # subprocess.call waits for completion and returns the exit code.
            return_code = subprocess.call(args, close_fds=False)
            sys.exit(return_code)
        else:
            # On Unix-like systems, replace the current Python process with the executable.
            # This is efficient and avoids stream handling issues in the wrapper.
            os.execl(executable_path, *args)
            # os.execl does not return if successful. If it does, an error occurred.
            # The following lines are only reached if execl fails.
            print(f"Error: Failed to execute '{executable_path}' using os.execl.", file=sys.stderr)
            sys.exit(1)

    except OSError as e:
        # Catch potential errors during execl or subprocess.call
        print(f"Error: Failed to execute '{executable_path}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()