"""
File: mylogger.py
Author: Scott Halgrim, halgrim.s@ghc.org
Date: 10/8/10
Functionality: Encapsulates initialization of logging
Contents:
    config - function that encapuslates initialization of logging
Notes:
    Here are some general notes on logging, which can get really confusing
    - each module can have a logger created for it
    - and that logger has ancestors that reflect the module heirarchy
    - when a logger gets a message, it checks the level against its level
    - if the level is equal to or higher than its level it handles it
      - it handles it by passing it to all its handlers and all the handlers of
        its ancestor loggers
      - note that those ancestor loggers don't care about the level, but their
        handlers do
      - so the message has to get over the threshold set by the logger on which
        its called and then it gets sent to all of that logger's handlers as
        well as all of its ancestors' handlers...and for each one of those
        handlers where it beats the threshold, it also gets output there
    - and if the root logger doesn't have a handler and it gets a message, it
      will create a handler with a level of 0, which can be annoying
    - this is further complicated by the fact that i often send messages to the
      root logger (e.g., logging.debug(), logging.warning()) and sometimes I
      send messages to the module logger (e.g., logger.debug(),
      logging.warning()).  I feel like I'm moving more to a module-level system,
      but can't be sure.
"""

import errno
import logging
import os
import sys


def mkdir_p(path):
    """
    Function: mkdir_p
    Input:
        path - the path of the dir to be created
    Output: none
    Functionality: Emulates mkdir -p functionality in unix which doesn't care
                   if a dir already exists and creates parent dirs if needed
    Author: TZ[omega]TZIOY
    Reference: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    History:
        7/15/11 - added WindowsError exception checking for
                  trunk\DelineNotes.bat and added the logging of exc.errno
    """
    try:
        os.makedirs(path)  # just make all dirs in path
    except OSError as exc:  # unless you get an error... # Python >3
        if exc.errno == errno.EEXIST:  # and that errors no is the path exists
            pass  # that you can ignore

        # if the problem is that path == ''
        elif exc.errno == errno.ENOENT and not path:
            pass  # then ignore that too
        else:  # otherwise
            # write errno to stderr
            print(sys.stderr, 'exc.errno: %d'.format(exc.errno))
            logging.error('exc.errno: %d'.format(exc.errno))  # log the errno
            raise  # and re-raise error


def logUncaughtExceptions(*exc_info):
    """
    Set sys.excepthook to this if you want to make sure a script-ending
    exception gets logged.  Otherwise that info tends to disappear.
    I got this script here:
    http://blog.tplus1.com/index.php/2012/08/05/python-log-uncaught-exceptions-with-sys-excepthook/
    I also have some stuffed tagged in bookmarks for getting pdb started when an
    exception like this happens.
    """
    logging.critical('Unhandled exception:', exc_info=exc_info)


def debugConfig(name):
    """
    Function: debugConfig
    Input: name - module to create logger for
    Output: logger - the logger created and configured for debug messaging
    Functionality: I believe I wrote this as an alternative to config below so
                   that you could get logging messages written to stdout, which
                   would be helpful during debugging.
    """

    # create at least some handler on root so you don't get duplicated
    # messages from debug handler
    rootlogger = logging.getLogger()  # obtain root logger

    # if something already handling logging on root, ignore this, but if not...
    if not rootlogger.handlers:
        # create a default handler to put on root
        defaultHandler = logging.StreamHandler()
        defaultHandler.setLevel(logging.WARNING)  # set its level to WARNING
        rootlogger.addHandler(defaultHandler)  # and add it to root logger

    logger = logging.getLogger(name)  # get this module's logger
    logger.setLevel(logging.DEBUG)  # set it to debug

    # set the message formatting
    debugFormatter = logging.Formatter('%(levelname) -9s %(asctime)s ' + \
                                       '%(module)s at line %(lineno)d: ' + \
                                       '%(message)s', '%H:%M')

    # create a stream handler for debug and assign to 
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(debugFormatter)  # give it the debugging format above
    sh.setLevel(logging.DEBUG)  # set its level to debug
    logger.addHandler(sh)  # add the handler to logger

    return logger  # and return the logger


def config(logfn='', loglevel=logging.WARNING, logmode='a'):
    """
    Function: config
    Input:
        logfn - logging filename
        loglevel - level at and above which to log messages
        logmode - logging mode.  e.g., a for append, w for write
    Output: none
    Functionality: Encapuslates initialization of logging
    """

    # if logging file provided, create path to it if it does not exist
    if logfn:
        mkdir_p(os.path.dirname(logfn))

    # configure logging
    logging.basicConfig(filename=logfn,
                        level=loglevel,
                        filemode=logmode,
                        format='%(levelname) -10s %(asctime)s %(module)s ' + \
                               'at line %(lineno)d: %(message)s')
