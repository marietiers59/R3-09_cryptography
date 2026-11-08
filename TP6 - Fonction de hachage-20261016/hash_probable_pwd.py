import argon2
import random


def main():
    with open("probable-v2_top-207.txt", "r", encoding="utf-8") as f:
        passwords = f.read().splitlines()

    # choose random passwords
    # seed = md5("Cryptographie").digest()
    seed = bytes.fromhex("f71dbe52628a3f83a77ab494817525c6")
    rng = random.Random(seed)
    num_passwords = len(passwords)
    num_chosen = 3

    chosen_indices = [rng.randrange(num_passwords) for _ in range(num_chosen)]
    passwords = [passwords[i] for i in chosen_indices]

    a2 = argon2.PasswordHasher()
    salts = [rng.randbytes(a2.salt_len) for _ in range(num_chosen)]

    hashes = [a2.hash(pwd, salt=salt) for pwd, salt in zip(passwords, salts)]
    with open("hashes-top-207.txt", "w", encoding="ascii") as f:
        f.write("\n".join(hashes))


if __name__ == "__main__":
    main()
