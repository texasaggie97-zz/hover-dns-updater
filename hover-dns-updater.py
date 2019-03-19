#!/usr/bin/env python

"""hover.py: Provides dynamic DNS functionality for Hover.com using their unofficial API.
   This script is based off one by Andrew Barilla: https://gist.github.com/andybarilla/b0dd93e71ff18303c059"""

__author__ = "Mark Silva"
__credits__ = ["Mark Silva", "Andrew Barilla", "Dan Krause"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Mark Silva"
__email__ = ""
__status__ = "Alpha"

import datetime
import json
import logging
import logging.handlers
import requests
import sys
import time
import os

import pprint
pp = pprint.PrettyPrinter(width=120)

default_config = {
    # Your hover.com username and password
    'username': 'ENV',
    'password': 'ENV',
    # Sign into hover.com and then go to: https://www.hover.com/api/domains/YOURDOMAIN.COM/dns
    # Look for the subdomain record(s) that you want to update and put its/their id(s) here.
    'dns_ids': ['ENV'],
    'logfile': 'ENV',
    'run-as-service': False,
    'poll-time': 600,  # 10 minutes
}


def configure_logging(lvl=logging.INFO, logfile=None):
    root = logging.getLogger()
    root.setLevel(lvl)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s:%(lineno)s)",
        "%Y-%m-%d %H:%M:%S")
    if logfile is None:
        hndlr = logging.StreamHandler(sys.stdout)
    else:
        print("Logging to file %s" % logfile)
        hndlr = logging.handlers.RotatingFileHandler(logfile, maxBytes=20000000, backupCount=5)
    hndlr.setFormatter(formatter)
    root.addHandler(hndlr)


class HoverConfig(object):
    def __init__(self, args):
        self._config = default_config
        try:
            with open(args.config_file, 'r') as c:
                config = json.load(c)
                for k in config:
                    self._config[k] = config[k]
        except FileNotFoundError:
            with open(args.config_file, 'w') as c:
                json.dump(default_config, c)
            sys.exit(1)

        # Override config file with command line parameters
        self.USERNAME = self._config['username']
        self.PASSWORD = self._config['password']
        self.DNS_IDS = self._config['dns_ids']
        self.LOGFILE = self._config['logfile'] if args.log_file is None else args.log_file
        self.SERVICE = self._config['run-as-service'] if args.service is None else args.service
        self.POLLTIME = self._config['poll-time'] if args.poll_time is None else args.poll_time

        if self.USERNAME == 'ENV':
            self.USERNAME = os.environ['USERNAME']
        if self.PASSWORD == 'ENV':
            self.PASSWORD = os.environ['PASSWORD']
        if self.LOGFILE == 'ENV':
            self.LOGFILE = os.environ['LOGFILE']
        if len(self.DNS_IDS) == 1 and self.DNS_IDS[0] == 'ENV':
            self.DNS_IDS = []
            i = 1
            # We expect the environment variable to be DNS1, DNS2, ... DNSn
            while True:
                try:
                    id = 'DNS{0}'.format(i)
                    self.DNS_IDS.append(os.environ[id])
                    i += 1
                except KeyError:
                    break

    def __repr__(self):
        ret_str = self.__class__.__name__ + '():\n'
        ret_str += '    USERNAME = {0}\n'.format(self.USERNAME)
        ret_str += '    PASSWORD = {0}\n'.format(self.PASSWORD)
        ret_str += '    DNS_IDS = {0}\n'.format(pp.pformat(self.DNS_IDS))
        ret_str += '    LOGFILE = {0}\n'.format(str(self.LOGFILE))
        ret_str += '    SERVICE = {0}\n'.format(str(self.SERVICE))
        ret_str += '    POLLTIME = {0}\n'.format(str(self.POLLTIME))
        return ret_str


class HoverException(Exception):
    pass


class HoverAPI(object):
    def __init__(self, config):
        self._config = config
        self._current_dns_ips = {}
        self.get_auth()
        self.get_current_ips()

    def get_auth(self):
        logging.info('Logging in')
        data = {"password": self._config.PASSWORD, "username": self._config.USERNAME, }
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        r = requests.post("https://www.hover.com/api/login", data=data_json, headers=headers)
        if not r.ok or "hoverauth" not in r.cookies:
            raise HoverException(r)
        self._cookies = {"hoverauth": r.cookies["hoverauth"]}
        self._auth_timestamp = datetime.datetime.now()

    def check_auth(self):
        td = datetime.datetime.now() - self._auth_timestamp
        # We will cache the login authorization for two hours
        if td.total_seconds() > (2 * 60 * 60):
            self.get_auth()

    def get_current_ips(self):
        logging.info('Getting current IP addresses from Hover:')
        current = self.call("get", "dns")
        for domain in current.get('domains'):
            for entry in domain['entries']:
                if entry['id'] in self._config.DNS_IDS:
                    logging.info('    {0} = {1}'.format(entry['id'], entry['content']))
                    self._current_dns_ips[entry['id']] = entry['content']

    def update(self):
        current_external_ip = requests.get('https://api.ipify.org').text
        logging.info('Updating - Current external IP = {0}'.format(current_external_ip))
        for dns_id in self._current_dns_ips:
            logging.debug('    {0} = {1}'.format(dns_id, self._current_dns_ips[dns_id]))
            if self._current_dns_ips[dns_id] != current_external_ip:
                logging.info('    Updating DNS entry for {0} to {1}'.format(dns_id, current_external_ip))
                self.call('put', 'dns/' + dns_id, {'content': current_external_ip})
                # Update cache
                self._current_dns_ips[dns_id] = current_external_ip

    def call(self, method, resource, data=None):
        logging.debug('method={0}, resource={1}, data={2}'.format(method, resource, str(data)))
        self.check_auth()
        url = "https://www.hover.com/api/{0}".format(resource)
        r = requests.request(method, url, data=data, cookies=self._cookies)
        if not r.ok:
            raise HoverException(r)
        if r.content:
            body = r.json()
            if "succeeded" not in body or body["succeeded"] is not True:
                raise HoverException(body)
            return body


def _parse_args(argv):
    import argparse
    parser = argparse.ArgumentParser()

    config_group = parser.add_argument_group("Configuration options")
    config_group.add_argument(
        "-c", "--config-file", default='hover-update.cfg', action="store",
        help="Config file, in json format. If it does not exist, one will be created with default values.")
    config_group.add_argument(
        "--service", default=False,
        action="store_true", help="Run as a service")
    config_group.add_argument(
        "--poll-time", default=None,
        action="store", help="Time in seconds to sleep between polling the ip address")

    verbosity_group = parser.add_argument_group("Verbosity, Logging & Debugging")
    verbosity_group.add_argument(
        "-v", "--verbose",
        action="count", default=0,
        help="Print debug information.  Can be repeated for more detailed output.")
    verbosity_group.add_argument(
        "-q", "--quiet",
        action="count", default=0,
        help="Print only essential information.  Can be repeated for quieter output.")
    verbosity_group.add_argument(
        "--test",
        action="store_true", default=False,
        help="Run doctests then quit.")
    verbosity_group.add_argument(
        "--log-file",
        action="store", default=None,
        help="Send logging to listed file instead of stdout")

    args = parser.parse_args(argv)

    # We want to default to WARNING
    # Verbosity gives us granularity to control past that
    if 0 < args.verbose and 0 < args.quiet:
        parser.error("Mixing --verbose and --quiet is contradictory")
    # We start logging level at INFO
    verbosity = 1 + args.quiet - args.verbose
    verbosity = max(verbosity, 0)
    verbosity = min(verbosity, 4)
    args.logging_level = {
        0: logging.DEBUG,
        1: logging.INFO,
        2: logging.WARNING,
        3: logging.ERROR,
        4: logging.CRITICAL,
    }[verbosity]

    if args.test:
        return args

    return args


def _main(config):
    client = HoverAPI(config)

    while True:
        try:
            client.update()
            # If we are not running as a service we only want to update once
            if not config.SERVICE:
                break

            logging.debug('Sleeping.... Z Z Z Z')
            time.sleep(config.POLLTIME)
        except KeyboardInterrupt:
            logging.info('Exiting from Control-C')
            break


def main():  # pragma: no cover
    import sys
    args = _parse_args(sys.argv[1:])
    config = HoverConfig(args)

    configure_logging(args.logging_level, config.LOGFILE)

    if args.test:
        # import doctest
        # print(doctest.testmod())
        pp.pprint(config)
        return 0

    ret_code = _main(config)
    sys.exit(ret_code)


if __name__ == "__main__":  # pragma: no cover
    main()
