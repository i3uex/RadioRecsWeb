import argparse
import logging
import os

import cherrypy

import constants as c
from WebServer import WebServer, MakePredictionService
from constants import *


def parse_arguments():
    program_description = "CompareFEFS Server"
    argument_parser = argparse.ArgumentParser(description=program_description)
    argument_parser.add_argument("-e", "--environment", help="name of the environment the server runs in")

    arguments = argument_parser.parse_args()

    environment = DEFAULT_ENVIRONMENT
    if arguments.environment:
        environment = arguments.environment

    return environment


def error_page_500(status, message, traceback, version):
    return f"{message}"


def setup_logging():
    logging.basicConfig(filename='log/debug.log', level=logging.DEBUG)


def start_server(environment):
    if not os.path.exists(c.LOG_PATH):
        os.makedirs(c.LOG_PATH)

    setup_logging()

    global_config_filename = f"global-{environment}.ini"
    cherrypy.config.update(global_config_filename)
    cherrypy.config.update({'error_page.500': error_page_500})

    webapp = WebServer()
    webapp.make_prediction = MakePredictionService()
    cherrypy.quickstart(webapp, '/', "app.ini")


def main():
    environment = parse_arguments()
    start_server(environment)


if __name__ == '__main__':
    main()
