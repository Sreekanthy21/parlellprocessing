"""
Created on Sep 10, 2014

@author sreekanthy21@gmail.com

Sreekanth Yekabathula

"""
import logging

def logger(file, msg, option):
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.FileHandler(file)
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    if option == "debug":
        logger.debug(msg)
    elif option == "info":
        logger.info(msg)
    elif option == "warn":
        logger.warn(msg)
    elif option == "error":
        logger.error(msg)
    else:
        logger.critical(msg)
    logger.removeHandler(ch)
if __name__ == "__main__":
    logger("temp.log", "Logger Message", "info")

