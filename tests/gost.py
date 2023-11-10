import binascii
import unittest

from pygost.gost3411_12 import GOST341112


class TestGOST341112(unittest.TestCase):
    def test_hash_function(self):
        M1 = b"01323130393837363534333231303938373635343332313039383736353433323130393837363534333231303938373635343332313039383736353433323130"
        correct_hash = '066a8f6264dce2e37169089b2f685d90bbff911dbc4f4ae36ced9c17d3e820a7'

        m = GOST341112(digest_size=256)
        m.update(M1)

        self.assertEqual(m.hexdigest(), correct_hash)

    def test_hex_conversion(self):
        hexed = 'eb4672c915b0e4f19ce949b9a8fff8ba6b36172ed168458d6a75e752e66faaf3'

        bytes_result = bytes.fromhex(hexed)
        decoded = binascii.hexlify(bytes_result).decode()

        self.assertEqual(decoded, hexed)



if __name__ == '__main__':
    unittest.main()
