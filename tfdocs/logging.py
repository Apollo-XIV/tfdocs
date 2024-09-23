import logging

def get_logger(name_override: str = __name__):
    logging.get_logger(name_override)
    
