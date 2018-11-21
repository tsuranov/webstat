#!/usr/bin/env python3
#######################################################################
#Логирование простое
#######################################################################
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log", level=logging.INFO)
 
logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")
#######################################################################
#Логирование правильное
# https://python-scripts.com/logging-python
# https://docs.python.org/3/howto/logging.html
# https://rtfm.co.ua/python-loggirovanie-s-pomoshhyu-modulya-logging/
####################################################################
import logging
import otherMod2
 
def main():
    """
    The main entry point of the application
    """
    
    logger = logging.getLogger("exampleApp")
    logger.setLevel(logging.INFO)
    
    # create the logging file handler
    fh = logging.FileHandler("new_snake.log")
 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    # add handler to logger object
    logger.addHandler(fh)
    
    logger.info("Program started")
    result = otherMod2.add(7, 8)
    logger.info("Done!")
 
if __name__ == "__main__":
    main()
#######################################################################
# otherMod2.py
import logging
 
module_logger = logging.getLogger("exampleApp.otherMod2")
 
def add(x, y):
    """"""
    logger = logging.getLogger("exampleApp.otherMod2.add")
    logger.info("added %s and %s to get %s" % (x, y, x+y))
    return x+y
#######################################################################
# В syslog
#######################################################################
import logging
import logging.handlers

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)

my_logger.debug('this is debug')
my_logger.critical('this is critical')

