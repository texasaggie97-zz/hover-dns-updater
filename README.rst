+----------------------+------------------------------------------------------------------------------------------------------------+
| master branch status | |BuildStatus| |Docs| |GPLLicense| |CoverageStatus|                                                         |
+----------------------+------------------------------------------------------------------------------------------------------------+
| GitHub status        | |OpenIssues| |OpenPullRequests|                                                                            |
+----------------------+------------------------------------------------------------------------------------------------------------+
| Versions             | 0.1.0.dev0                                                                                                 |
+----------------------+------------------------------------------------------------------------------------------------------------+

===========  ===========================================================================================================================
Info         Hover DNS Updater for Dynamic IP. See `GitHub <https://github.com/texasaggie97/hover-dns-updater/>`_ for the latest source.
Author       Mark Silva  (based on a script from `GitHub <https://gist.github.com/andybarilla/b0dd93e71ff18303c059>`_ by Andrew Barilla)
===========  ===========================================================================================================================

.. _about-section:

About
=====

**hover-dns-updater** will update the Hover DNS entries for one or more DNS records based on the external IP address. **hover-dns-updater** can do this one time or
can run continuously checking after a certain amount of time.

.. _installation-section:

Installation
============

Prerequisites:
--------------

* Python 3
    * `Download <https://www.python.org/downloads/>`_
* pip3
    * Linux - `sudo apt-get install -y python3-pip`
    * Windows - `python -m ensurepip --upgrade`
* Installed packages
    * requests
        * Linux - `sudo pip3 install --upgrade requests`
        * Windows - `pip install --upgrade requests`
    * ipgetter
        * Linux - `sudo pip3 install --upgrade ipgetter`
            * Windows - `pip install --upgrade ipgetter`

Hover DNS IDs:
--------------

* Login to `Hover.com <https://hover.com>`_
* In the same browser go to `https://www.hover.com/api/domains/YOURDOMAIN.COM/dns` replacing YOURDOMAIN.COM with the domain you want to update
* This will return a json file. If you use Firefox, this will be nicely formatted.
* In the "entries" list, look for the DNS records you want to keep up to date and make a note of the associated "id"s. They should look something like "dns1234567"

Install Ubuntu service:
-----------------------

* Copy `INSTALL.sh`, `hover-dns-updater.service`, and `hover-dns-updater.py` to a folder on you Ubuntu system
* `./INSTALL.sh`
* This will install and enable, but not start, the hover-dns-updater service
* `sudo nano /etc/hover-dns-updater/hover-dns-updater.json` (or use the editor of your choice)
    * Fill in your hover username and password
    * Add the dns ids you noted above
    * Optional - change `None` to the log file name
    * Optional - change poll time, in seconds. Default is 10 minutes
    * When running as an Ubuntu service, the service value in the confg file is ignored.
* After configuration file is updated, start the service `sudo service hover-dns-updater start`
* Option - Verify service started correctly `sudo service hover-dns-updater status`


Contributing
============

Contributions are welcome!

.. _bugs-section:

Bugs / Feature Requests
=======================

To report a bug or submit a feature request, please use the
`GitHub issues page <https://github.com/texasaggie97/hover-dns-updater/issues>`_.

License
=======

**hover-dns-updater** is licensed under an GPL-style license (`see
LICENSE <https://github.com/texasaggie97/hover-dns-updater/blob/master/LICENSE>`_).
Other incorporated projects may be licensed under different licenses.

.. |BuildStatus| image:: https://img.shields.io/travis/texasaggie97/hover-dns-updater.svg
    :alt: Build Status - master branch
    :target: https://travis-ci.org/texasaggie97/hover-dns-updater

.. |Docs| image:: https://readthedocs.org/projects/hover-dns-updater/badge/?version=latest
    :alt: Documentation Status - master branch
    :target: https://hover-dns-updater.readthedocs.io/en/latest/?badge=latest

.. |GPLLicense| image:: https://img.shields.io/badge/License-GPL-yellow.svg
    :alt: GPL License
    :target: https://opensource.org/licenses/gpl-license

.. |CoverageStatus| image:: https://coveralls.io/repos/github/ni/nimi-python/badge.svg?branch=master&dummy=no_cache_please_1
    :alt: Test Coverage - master branch
    :target: https://coveralls.io/github/ni/nimi-python?branch=master

.. |OpenIssues| image:: https://img.shields.io/github/issues/texasaggie97/hover-dns-updater.svg
    :alt: Open Issues + Pull Requests
    :target: https://github.com/texasaggie97/hover-dns-updater/issues

.. |OpenPullRequests| image:: https://img.shields.io/github/issues-pr/texasaggie97/hover-dns-updater.svg
    :alt: Open Pull Requests
    :target: https://github.com/texasaggie97/hover-dns-updater/pulls

