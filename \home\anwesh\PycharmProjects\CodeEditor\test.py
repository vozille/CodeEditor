def factorize(n):
    factors = []
    k = int( n**0.5) + 1
    for i in range(1, k):
        if n%i == 0:
            factors.append(n//i)
            if n//i != i:
                factors.append(i)
    return factors.sort()

num = input()
print factorize(num)