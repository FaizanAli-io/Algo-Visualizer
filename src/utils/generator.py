import random


def generate_coordinates(n: int, root: str) -> None:
    coordinates = [
        (
            random.randint(-100, 100),
            random.randint(-100, 100),
        )
        for _ in range(n)
    ]

    with open(f"{root}{n}.txt", "w") as file:
        for x, y in coordinates:
            file.write(f"({x}, {y})\n")


for num in range(100, 300, 20):
    root = "inputs\\closest_points\\"
    # generate_coordinates(num, root)
