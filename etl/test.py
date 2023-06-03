from datetime import datetime

data_chunk = [
    ['test1@test.com', '10', 'review for all1', '2023-06-02 17:22:17.530000'],
    ['test2@test.com', '0', 'review for all2', '2024-06-02 17:22:17.530000'],
    ['test3@test.com', '2', 'review for all3', '2025-06-02 17:22:17.530000'],
    ['test4@test.com', '4', 'review for all4', '2026-06-02 17:22:17.530000'],
]


mapped_numbers = list(map(lambda x: [
    x[0], int(x[1]), x[2], datetime.strptime(x[3].strip().split('.')[0], '%Y-%m-%d %H:%M:%S')
], data_chunk))

print(mapped_numbers)

