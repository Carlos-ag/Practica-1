
userText, timedOut = timedInput("Please, do enter something: ")
if(timedOut):
    print("Timed out when waiting for input.")
    print(f"User-input so far: '{userText}'")
else:
    print(f"User-input: '{userText}'")