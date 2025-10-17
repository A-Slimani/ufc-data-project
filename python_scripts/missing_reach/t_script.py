from rapidfuzz import fuzz

s1 = "shayna-baszler-the-queen-of-spades"
s2 = "baszler-the-queen-of-spades"

print(fuzz.ratio(s1, s2) / 100.0)
