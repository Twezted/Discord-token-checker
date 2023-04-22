import requests
import tkinter as tk

TOKEN_CHECK_ENDPOINT = "https://discordapp.com/api/v9/users/@me"

def check_token(token, proxies=None):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    response = requests.get(TOKEN_CHECK_ENDPOINT, headers=headers, proxies=proxies)

    if response.status_code == 200:
        return True
    else:
        return False

def check_tokens():
    with open("tokens.txt", "r") as f:
        tokens = f.read().splitlines()

    valid_tokens = []
    invalid_tokens = []

    with open("valid.txt", "w") as valid_file, open("invalid.txt", "w") as invalid_file:
        for token in tokens:
            proxy = proxy_entry.get()
            if proxy:
                proxy_parts = proxy.split(":")
                proxies = {
                    "http": f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}",
                    "https": f"http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}"
                }
            else:
                proxies = None

            if check_token(token, proxies):
                valid_tokens.append(token)
                valid_file.write(token + "\n")
            else:
                invalid_tokens.append(token)
                invalid_file.write(token + "\n")

    valid_tokens_label.config(text=f"Valid tokens: {len(valid_tokens)}")
    invalid_tokens_label.config(text=f"Invalid tokens: {len(invalid_tokens)}")

root = tk.Tk()
root.title("Token Checker")

tk.Label(root, text="Proxy (optional)").grid(row=0, column=0, padx=5, pady=5)
proxy_entry = tk.Entry(root)
proxy_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Button(root, text="Check Tokens", command=check_tokens).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

valid_tokens_label = tk.Label(root, text="Valid tokens: 0")
valid_tokens_label.grid(row=2, column=0, padx=5, pady=5)

invalid_tokens_label = tk.Label(root, text="Invalid tokens: 0")
invalid_tokens_label.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
