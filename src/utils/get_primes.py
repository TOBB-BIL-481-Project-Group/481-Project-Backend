primes = None
non_primes = None
vis_primes = [0] * (1000000 + 5)


def calculate_primes():
    global primes, non_primes
    if primes != None:
        return primes, non_primes

    primes = []
    non_primes = [0, 1]
    maxPrime = 1000000
    vis_primes[0] = 1
    vis_primes[1] = 1

    for i in range(2, maxPrime + 1):
        if vis_primes[i] == 1:
            non_primes.append(i)
            continue
        primes.append(i)
        for j in range(2 * i, maxPrime + 1, i):
            vis_primes[j] = 1

    return primes, non_primes


def is_prime(value):
    if value > 1e6 + 1:
        return False
    return vis_primes[value] == 0
