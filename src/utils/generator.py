import random


def generate_coordinates(n: int, root: str, suffix: int) -> None:
    coordinates = [
        (
            random.randint(0, 980) + 50,
            random.randint(0, 500) + 50,
        )
        for _ in range(n)
    ]

    with open(f"{root}{n} ({suffix}).txt", "w") as file:
        for x, y in coordinates:
            file.write(f"({x}, {y})\n")


def generate_binary_pairs(file_name, bit_size, count=100):
    with open(file_name, "w") as f:
        for _ in range(count):
            binary1 = f"{random.getrandbits(bit_size):0{bit_size}b}"
            binary2 = f"{random.getrandbits(bit_size):0{bit_size}b}"
            f.write(f"{binary1}, {binary2}\n")


def handler_points():
    points = [100, 100, 125, 125, 150, 150, 175, 175, 200, 200]
    prev_num = None

    for num in points:
        if prev_num and prev_num == num:
            suffix += 1
        else:
            suffix = 1

        prev_num = num

        root = "src\\inputs\\closest_points\\"
        generate_coordinates(num, root, suffix)


def handler_binary():
    for num in range(1, 11):
        bits = num * 16
        root = "src\\inputs\\integer_mult\\"
        generate_binary_pairs(f"{root}{bits}.txt", bits)
