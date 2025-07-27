import sys

def get_serial(username):
	if len(username) < 6:	
		raise ValueError("Username must be at least 6 characters")
	serial = (ord(username[3]) ^ 0x1337) + 0x5eeded
	for c in username:
		if ord(c) < 32:
			raise ValueError("Invalid character in username")
			serial += (ord(c) ^ serial) % 0x539
	return serial

username = "hacker"
password = get_serial(username)
print(f"Username: {username}")
print(f"Password: {password}")