import re
import secrets
import string
COMMON_PASSWORDS = {
    "password", "password123", "admin", "admin123",
    "123456", "12345678", "123456789", "qwerty",
    "welcome", "iloveyou", "letmein", "abc123",
    "monkey", "dragon", "football", "master"
}
KEYBOARD_PATTERNS = [
    "qwerty", "asdfgh", "zxcvbn",
    "123456", "654321", "qwertyui"
]
def check_password(password):
    score = 0
    suggestions = []
    warnings = []
    if not password:
        return "Weak", 0, ["Enter a password."], []
    if len(password) > 128:
        return "Weak", 0, ["Password is too long."], []
    lower = password.lower()
    if lower in COMMON_PASSWORDS:
        warnings.append("Common password detected.")
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 12 characters.")
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")
    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add numbers.")
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append("Add special characters.")
    if re.search(r"(.)\1{2,}", password):
        score -= 2
        warnings.append("Repeated characters detected.")
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789"
    ]
    if any(
        any(seq[i:i+4] in lower for i in range(len(seq)-3))
        for seq in sequences
    ):
        score -= 2
        warnings.append("Sequential characters detected.")
    if any(pattern in lower for pattern in KEYBOARD_PATTERNS):
        score -= 2
        warnings.append("Keyboard pattern detected.")
    if lower in COMMON_PASSWORDS:
        score = 0
    score = max(0, min(score, 6))
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"
    if warnings:
        suggestions.append("Avoid predictable password patterns.")
    return strength, score, suggestions, warnings
def generate_password():
    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*"
    )
    while True:
        password = ''.join(
            secrets.choice(characters) for _ in range(20)
        )
        strength, score, _, warnings = check_password(password)
        if strength == "Strong" and not warnings:
            return password
def main():
    print("=" * 45)
    print("       PASSWORD SECURITY AUDITOR")
    print("=" * 45)
    password = input("\nEnter password to test: ")
    strength, score, suggestions, warnings = check_password(password)
    print("\nPassword Strength:", strength)
    print("Security Score:", score, "/ 6")
    if warnings:
        print("\nSecurity Warnings:")
        for warning in warnings:
            print("[-]", warning)
    if suggestions:
        print("\nSuggestions:")
        for suggestion in suggestions:
            print("[+]", suggestion)
    else:
        print("\nAll basic security checks passed.")
    if strength != "Strong":
        print("\nSuggested Password:", generate_password())
    print("\n" + "=" * 45)
    print("SECURITY CHECK COMPLETED")
    print("=" * 45)
if __name__ == "__main__":
    main()
