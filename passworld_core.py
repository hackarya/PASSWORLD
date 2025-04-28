import math
import requests
import hashlib

def check_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 12 and score == 4:
        return "Strong"
    elif length >= 8 and score >= 2:
        return "Moderate"
    else:
        return "Weak"

def estimate_crack_time(password):
    chars = 0
    if any(c.islower() for c in password):
        chars += 26
    if any(c.isupper() for c in password):
        chars += 26
    if any(c.isdigit() for c in password):
        chars += 10
    if any(not c.isalnum() for c in password):
        chars += 32

    total_combinations = chars ** len(password)
    guesses_per_second = 1e9  # Very fast attacker
    seconds = total_combinations / guesses_per_second

    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 2592000:
        return f"{int(seconds/86400)} days"
    elif seconds < 31536000:
        return f"{int(seconds/2592000)} months"
    else:
        return f"{int(seconds/31536000)} years"

def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() for c in password):
        pool += 32
    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def check_breach(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if suffix in response.text:
        return "Yes (Breached!)"
    else:
        return "No (Safe)"