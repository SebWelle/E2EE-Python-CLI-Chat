from nacl.public import PrivateKey
from nacl.public import Box

def generate_keypair():
    private_key = PrivateKey.generate()
    public_key = private_key.public_key
    
    print("Private Key:", private_key.encode().hex())
    print("Public Key:", public_key.encode().hex())
    
    return private_key, public_key



if __name__ == "__main__":
    alice = generate_keypair()
    bob = generate_keypair()

    box1 = Box( alice[0], bob[1])

    message = "I am an encrypted message"

    cipher_bytes = message.encode('utf-8')
    cipher = box1.encrypt(cipher_bytes)

    print(cipher)

    box2 = Box(bob[0], alice[1])

    plain_bytes = box2.decrypt(cipher)
    plain = plain_bytes.decode('utf-8')

    print(plain)




