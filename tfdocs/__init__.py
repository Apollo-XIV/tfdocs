from tfdocs.logging import get_logger

log = get_logger(stream=True)

def main():
    log.critical("Oh my god its a message!")
