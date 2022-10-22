import random
import time

from longest_increasing_subsequence import longest_increasing_subsequence


def generate_random_list() -> list[int]:
    return [random.randint(0, 1000000001) for _ in range(20000)]


arr = generate_random_list()
t = time.time()
seq = longest_increasing_subsequence(arr)
print("Length of lis is", len(seq))
print(f"seconds: {time.time() - t}")
