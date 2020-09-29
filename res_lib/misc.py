import logging
import os


def get_logger(logger_name, logfile,
               file_loglevel=logging.INFO,
               console_loglevel=logging.ERROR):
    """
    Create instance of logger, written to logfile.
    Logging to file is set to DEBUG level by default, but this can be raised or
    lowered when logger is created.

    This logger will by default print ERROR and above to the console, and DEBUG
    or above to the specified logfile.
    """
    # Check if logfile and directory exists
    for i in range(len(logfile.split("/"))):
        path = "/".join(logfile.split("/")[:i+1])
        if not os.path.exists(path):
            if "." in path:
                open(path, 'a').close()
            else:
                os.mkdir(path)
    # set up logging to file
    logging.basicConfig(level=file_loglevel,
                        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y%m%d %H:%M:%S',
                        filename=logfile,
                        filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(console_loglevel)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(name=logger_name)
    return logger
