
def hello_world(name: str = "world") -> str:
    if name == "":
        name = "world"
    return f"hello, {name}!"
