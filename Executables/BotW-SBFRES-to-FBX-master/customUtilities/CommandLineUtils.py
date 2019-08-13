# Better than os.system for CL arguments.
import subprocess

# Used for command line arguments.
def quoted(string: str):
    quote = "\""
    return quote + string + quote

# Utility method to call something via command prompt.
def call(item: str, args: list):
    argsString = ""
    for arg in args:
        argsString += " " + arg

    # DO NOT REMOVE stdout.read() BELOW
    print("Calling " + item + argsString)
    subprocess.Popen(item + argsString, shell=True, stdout=subprocess.PIPE).stdout.read()

def toQuotedPath(path: str):
    return quoted(path).replace("\\", "\\\\")