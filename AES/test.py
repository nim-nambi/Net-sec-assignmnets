import unittest
from aes_fun import AES
 
class AES_TEST(unittest.TestCase):
    def setUp(self):
        secret_key = 0x2b7e151628aed2a6abf7158809cf4f3c
        self.AES = AES(secret_key)
 
    def test_decryption(self):
        ciphertxt = 0x3925841d02dc09fbdc118597196a0b32
        decrypted = self.AES.decrypt(ciphertxt)
 
        self.assertEqual(decrypted, 0x3243f6a8885a308d313198a2e0370734)

    def test_encryption(self):
        plaintxt = 0x3243f6a8885a308d313198a2e0370734
        encrypted = self.AES.encrypt(plaintxt)
 
        self.assertEqual(encrypted, 0x3925841d02dc09fbdc118597196a0b32) 
 
if __name__ == '__main__':
    unittest.main()
