from math import log2

BLOCK_WIDTH = 1600                  # permutation block width b
BIT_RATE = 1088                     # rate r
OUTPUT_LENGTH = 256                 # output length d
CAPACITY = 512                      # capacity c
WORD_SIZE = int(BLOCK_WIDTH/25)     # word size w
WORD_POWER = int(log2(WORD_SIZE))   # power of two l
