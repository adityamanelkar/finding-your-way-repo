# Module to read the reactor map in reactor.txt

def read(filename: str) -> list:
    """
    Reads the reactor.txt file and converts it to a 2D Array
    """
    with open(filename) as f:
        lines = f.read().splitlines()

    return [list(line) for line in lines]

# For test pruposes
if __name__ == "__main__":
    filename = "./reactor.txt"
    print("The matrix read by the read() function is:\n{}".format(read(filename)))