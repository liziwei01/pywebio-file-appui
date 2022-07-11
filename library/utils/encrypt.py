'''
Author: liziwei01
Date: 2022-07-10 16:03:22
LastEditors: liziwei01
LastEditTime: 2022-07-10 17:54:06
Description: file content
'''
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

def EncryptRsa(password: str) -> str:
	public_key = open(getRSAKeyPath(), "r").read()
	encrypted = _encrpt_rsa(password, public_key)
	return encrypted

def _encrpt_rsa(password: str, public_key: str) -> str:
	first_base64_encrypted = base64.b64encode(password.encode())
	rsakey = RSA.importKey(public_key)
	cipher = Cipher_pksc1_v1_5.new(rsakey)
	second_rsa_encrypted = cipher.encrypt(first_base64_encrypted)
	third_base64_encrypted = base64.b64encode(second_rsa_encrypted)
	return third_base64_encrypted.decode()

def getRSAKeyPath() -> str:
	return "/conf/pem/rsa_public_key.pem"