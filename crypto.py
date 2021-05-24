#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from argparse import ArgumentParser
from cryptography.fernet import Fernet, InvalidToken
import base64
import os
import sys


class Cryptography:
    def __init__(self, log):
        self.log = log
        self.private_key = "sMZo38VwRdigN78FBnHj8mETNlofL4Qhj_x5cvyxJsc="
        self.cipher_suite = Fernet(bytes(self.private_key, "UTF-8"))


    @staticmethod
    def generate_private_key():
        private_key = base64.urlsafe_b64encode(os.urandom(32))
        return private_key


    def encode(self, passw):
        str_bytes = bytes(passw, "UTF-8")
        encoded_text = self.cipher_suite.encrypt(str_bytes)
        return encoded_text


    def decode(self, encoded_text):
        if encoded_text is not None and len(encoded_text) > 0:
            try:
                et = bytes(encoded_text, "UTF-8")
                decoded_text = self.cipher_suite.decrypt(et)
                return str(decoded_text.decode("UTF-8"))
            except InvalidToken:
                msg = f"ERRO ao decriptar. Password nao esta encriptado: {encoded_text}"
                if len(encoded_text) == 100:
                    msg = f"ERRO ao decriptar. Password foi encriptado com outra private key: {encoded_text}"

                if self.log is not None:
                    self.log.info(msg)
                else:
                    sys.stderr.write(f"ERROR: {msg}\n")
        return ""


if __name__ == "__main__":
    parser = ArgumentParser(prog="Cryptography", add_help=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encriptar", type=str, help="Encriptar uma string")
    group.add_argument("-d", "--decriptar", type=str, help="Decriptar uma string")
    group.add_argument("-k", "--key", action="store_true", help="Gerar Private key")
    args = parser.parse_args()
    crypt = Cryptography(None)

    if args.encriptar:
        enc = crypt.encode(args.encriptar)
        if len(enc) > 0:
            print(f"Encriptado: {enc.decode('utf-8')}")
    elif args.decriptar:
        enc = crypt.decode(args.decriptar)
        if len(enc) > 0:
            print(f"Decriptado: {enc}")
    elif args.key:
        pk = crypt.generate_private_key()
        print(f"Private Key: {pk.decode('utf-8')}")
