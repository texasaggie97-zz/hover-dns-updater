| | |
| --- | --- |
| master branch status | ![Build Status - master branch]](https://img.shields.io/travis/texasaggie97/hover-dns-updater.svg "Build Status - master branch") ![Documentation Status - master branch](https://readthedocs.org/projects/hover-dns-updater/badge/?version=latest "Documentation Status - master branch") ![GPL License](https://img.shields.io/badge/License-GPL-yellow.svg "GPL License") ![Test Coverage - master branch](https://coveralls.io/repos/github/ni/nimi-python/badge.svg?branch=master&dummy=no_cache_please_1 "Test Coverage - master branch") |
| GitHub status | ![Open Issues + Pull Requests](https://img.shields.io/github/issues/texasaggie97/hover-dns-updater.svg "Open Issues + Pull Requests") ![Open Pull Requests](https://img.shields.io/github/issues-pr/texasaggie97/hover-dns-updater.svg "Open Pull Requests") |
| Versions | 0.1.0.dev0 |

| | |
| --- | --- |
| Info | Hover DNS Updater for Dynamic IP. See [GitHub](https://github.com/texasaggie97/hover-dns-updater/)  for the latest source. |
| Author | Mark Silva, based on a script from [GitHub](https://gist.github.com/andybarilla/b0dd93e71ff18303c059) by Andrew Barilla |

About
=====

**hover-dns-updater** will update the Hover DNS entries for one or more
DNS records based on the external IP address. **hover-dns-updater** can
do this one time or can run continuously checking after a certain amount
of time.

Installation
============

Prerequisites:
--------------

-   Python 3  
    -   [Download](https://www.python.org/downloads/)

-   pip3  
    -   Linux - sudo apt-get install -y python3-pip
    -   Windows - python -m ensurepip --upgrade

-   Installed packages  
    -   requests  
        -   Linux - sudo pip3 install --upgrade requests
        -   Windows - pip install --upgrade requests

    -   ipgetter  
        -   Linux - sudo pip3 install --upgrade ipgetter  
            -   Windows - pip install --upgrade ipgetter

Hover DNS IDs:
--------------

-   Login to [Hover.com](https://hover.com)
-   In the same browser go to
    https://www.hover.com/api/domains/YOURDOMAIN.COM/dns replacing
    YOURDOMAIN.COM with the domain you want to update
-   This will return a json file. If you use Firefox, this will be
    nicely formatted.
-   In the "entries" list, look for the DNS records you want to keep up
    to date and make a note of the associated "id"s. They should look
    something like "dns1234567"

Install Ubuntu service:
-----------------------

-   Copy INSTALL.sh, hover-dns-updater.service, and hover-dns-updater.py
    to a folder on you Ubuntu system
-   ./INSTALL.sh
-   This will install and enable, but not start, the hover-dns-updater
    service
-   sudo nano /etc/hover-dns-updater/hover-dns-updater.json (or use the editor of your choice)  
    -   Fill in your hover username and password
    -   Add the dns ids you noted above
    -   Optional - change None to the log file name
    -   Optional - change poll time, in seconds. Default is 10 minutes
    -   When running as an Ubuntu service, the service value in the
        confg file is ignored.

-   After configuration file is updated, start the service
    sudo service hover-dns-updater start
-   Option - Verify service started correctly
    sudo service hover-dns-updater status

Create Docker container
-----------------------

>     docker build -t hover-dns-updater . ; docker tag hover-dns-updater texasaggie97/hover-dns-updater:latest ; docker push texasaggie97/hover-dns-updater

RancherOS
---------

I am using RancherOS to host and manage Docker running in a lightweight
VM on FreeNAS. Here are the docker-compose.yml and rancher-compose.yml
to easily recreate the container.

### docker-compose.yml:

>     version: '2'
>     volumes:
>         logs:
>             external: true
>             driver: rancher-nfs
>
>     services:
>         alarmserver:
>             image: texasaggie97/alarmserver
>             environment:
>                 ALARMCODE: "1234"
>                 CALLBACKURL_BASE: "https://graph.api.smartthings.com/api/smartapps/installations"
>                 CALLBACKURL_APP_ID: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
>                 CALLBACKURL_ACCESS_TOKEN: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
>                 LOGFILE: "/logs/docker-alarmserver.log"
>                 ENVISALINKHOST: "192.168.0.149"
>             stdin_open: true
>             working_dir: /alarmserver
>             volumes:
>             - logs:/logs
>             tty: true
>             ports:
>             - 8111:8111/tcp
>             command:
>             - python
>             - alarmserver.py
>             labels:
>                 io.rancher.container.pull_image: always
>
>         hover-dns-updater:
>             image: texasaggie97/hover-dns-updater
>             environment:
>                 USERNAME: "username"
>                 PASSWORD: "password"
>                 DNS1: "dns00000000"
>                 DNS2: "dns00000001"
>                 LOGFILE: "/logs/docker-hover-dns-updater.log"
>             stdin_open: true
>             working_dir: /hover-dns-updater
>             volumes:
>             - logs:/logs
>             tty: true
>             command:
>             - python
>             - hover-dns-updater.py
>             - --service
>             labels:
>                 io.rancher.container.pull_image: always

### rancher-compose.yml:

>     version: '2'
>     services:
>         alarmserver:
>             scale: 1
>             start_on_create: true
>         hover-dns-updater:
>             scale: 1
>             start_on_create: true

Contributing
============

Contributions are welcome!

Bugs / Feature Requests
=======================

To report a bug or submit a feature request, please use the [GitHub
issues page](https://github.com/texasaggie97/hover-dns-updater/issues).

License
=======

**hover-dns-updater** is licensed under an GPL-style license ([see
LICENSE](https://github.com/texasaggie97/hover-dns-updater/blob/master/LICENSE)).
Other incorporated projects may be licensed under different licenses.
