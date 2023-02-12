start = 3950000
step = 270000
for i in range(53, 110):
    print((start + step) // 10000 * 10000)
    step += 100000
    step *= 1.1
