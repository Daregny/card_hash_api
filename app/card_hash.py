from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from urllib.parse import urlencode, quote_plus, quote
import base64
import urllib
import pagarme


pagarme.authentication_key("SUA_ENCRYPTION_KEY")
#

card_hash_key = pagarme.transaction.generate_card_hash_key()

publickey = card_hash_key["public_key"]
id = card_hash_key["id"]


def card_hash(data):
    message = urlencode(data, quote_via=quote)
    key = RSA.importKey(publickey)

    cipher = PKCS1_v1_5.new(key)
    ciphertext = cipher.encrypt(bytes(message, "utf-8"))
    res_base64 = base64.b64encode(ciphertext)

    hash = str(id) + "_" + str(res_base64).replace("b'", '').replace("'", '')

    return hash

