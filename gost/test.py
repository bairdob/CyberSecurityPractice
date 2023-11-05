import codecs
import time

from gost import utils
from gost.GOST import GOST

gost = GOST()
msg = "Hello, world!"
msg = "Meeting at 3 PM"
key, salt = utils.pbkdf2("Hallelujah", "", iter=100000)
t1 = time.time()
gost.set_message(utils.string_to_bytes(msg))
print(utils.string_to_bytes(msg))
gost.set_key(key)
gost.set_operation_mode(gost.CFB)
print("Msg: ", msg)
print("Key: ", utils.leading_zeros_hex(key))
print("Salt: ", salt)
ciphertext = utils.leading_zeros_hex(gost.encrypt())
print("IV: ", utils.leading_zeros_hex(gost.get_iv()))
print("Encrypted: ", ciphertext)
t2 = time.time()
print("Elapsed time (s): ", t2 - t1)
print("Decrypted from scratch: ", utils.bytes_to_string(gost.decrypt()))
