def greet(name: str) -> None:
    print(f"Hello, {name}!")


def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    greet("Katerina")
    print(add(5, 3))