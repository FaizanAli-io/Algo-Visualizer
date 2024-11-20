import random


def generate_coordinates(n: int, root: str, suffix: int) -> None:
    coordinates = set()

    while len(coordinates) < n:
        coordinates.add(
            (
                random.randint(0, 980) + 50,
                random.randint(0, 500) + 50,
            )
        )

    with open(f"{root}{n} ({suffix}).txt", "w") as file:
        for x, y in coordinates:
            file.write(f"({x}, {y})\n")


def generate_integer_pairs(file_name, digits, count=100):
    start = 10 ** (digits - 1)
    limit = 10 ** (digits) - 1
    with open(file_name, "w") as f:
        for _ in range(count):
            integer1 = random.randint(start, limit)
            integer2 = random.randint(start, limit)
            f.write(f"{integer1}, {integer2}\n")


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


def handler_integer():
    for i in range(1, 11):
        size = str(i * 8).zfill(2)
        root = "src\\inputs\\integer_mult\\"
        generate_integer_pairs(f"{root}{size}.txt", int(size))
