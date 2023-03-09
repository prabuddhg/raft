import os
import operations as op
from functools import lru_cache
import logging

log = logging.getLogger(__name__)

@lru_cache
def get_file():
    curr_dir = os.getcwd()
    key_store = os.path.join(curr_dir, "key_store")
    return key_store


def save(input):
    if "set" in input or "del" in input:
        log.info(f"Saving {input}")
        with open(get_file(), "a") as ks:
            ks.write(f"{input}\n")
    else:
        log.info(f"Skipping {input}")


def process(input):
    save(input)
    return op.execute(input)


def recover():
    with open(get_file(), "r") as ks:
        file_line = ks.readline()
        while file_line:
            log.info(f"Processing {file_line}")
            if "set" in file_line or "del" in file_line:
                log.info(f"Recovering {file_line}")
                op.execute(file_line)
            else:
                log.info(f"Skipping {file_line}")
            # use realine() to read next line
            file_line = ks.readline()
