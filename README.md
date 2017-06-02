<p align="center"><a href="https://pyload.net"><img src="/media/banner.png" alt="pyLoad" /></a></p>

WebUI module of [**pyLoad**](https://github.com/pyload/pyload),
*The Free and Open Source download manager written in Pure Python and designed
to be extremely lightweight, fully customizable and remotely manageable*.

> **Notice:**
> [Master Branch](https://github.com/pyload/webui/tree/master) is under heavy
> development, very unstable, often broken. **Please, do not use it for now!**

**Release Status**:

[![Build Status](https://travis-ci.org/pyload/webui.svg?branch=master)](https://travis-ci.org/pyload/webui)
[![Requirements Status](https://requires.io/github/pyload/webui/requirements.svg?branch=master)](https://requires.io/github/pyload/webui/requirements/?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/pyload/webui/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/pyload/webui/?branch=master)
[![PyPI Status](https://img.shields.io/pypi/status/pyload.webui.svg)](https://pypi.python.org/pypi/pyload.webui)
[![PyPI Version](https://img.shields.io/pypi/v/pyload.webui.svg)](https://pypi.python.org/pypi/pyload.webui)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/pyload.webui.svg)](https://pypi.python.org/pypi/pyload.webui)

**Licensing**:

[![CLA assistant](https://cla-assistant.io/readme/badge/pyload/webui)](https://cla-assistant.io/pyload/webui)
[![PyPI License](https://img.shields.io/pypi/l/pyload.webui.svg)](https://pypi.python.org/pypi/pyload.webui)

**Contact Us** on:

[![pyload.net](https://img.shields.io/badge/.net-pyload-orange.svg)](https://pyload.net)
[![Twitter](https://img.shields.io/badge/-twitter-429cd6.svg?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiA%2FPjwhRE9DVFlQRSBzdmcgIFBVQkxJQyAnLS8vVzNDLy9EVEQgU1ZHIDEuMC8vRU4nICAnaHR0cDovL3d3dy53My5vcmcvVFIvMjAwMS9SRUMtU1ZHLTIwMDEwOTA0L0RURC9zdmcxMC5kdGQnPjxzdmcgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgMzIgMzIiIGhlaWdodD0iMzJweCIgaWQ9IkxheWVyXzEiIHZlcnNpb249IjEuMCIgdmlld0JveD0iMCAwIDMyIDMyIiB3aWR0aD0iMzJweCIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI%2BPHBhdGggZD0iTTMxLjk5Myw2LjA3N0MzMC44MTYsNi42LDI5LjU1Miw2Ljk1MywyOC4yMjMsNy4xMWMxLjM1NS0wLjgxMiwyLjM5Ni0yLjA5OCwyLjg4Ny0zLjYzICBjLTEuMjY5LDAuNzUxLTIuNjczLDEuMjk5LTQuMTY4LDEuNTkyQzI1Ljc0NCwzLjc5NywyNC4wMzgsMywyMi4xNDksM2MtMy42MjUsMC02LjU2MiwyLjkzOC02LjU2Miw2LjU2MyAgYzAsMC41MTQsMC4wNTcsMS4wMTYsMC4xNjksMS40OTZDMTAuMzAxLDEwLjc4NSw1LjQ2NSw4LjE3MiwyLjIyNyw0LjIwMWMtMC41NjQsMC45Ny0wLjg4OCwyLjA5Ny0wLjg4OCwzLjMgIGMwLDIuMjc4LDEuMTU5LDQuMjg2LDIuOTE5LDUuNDY0Yy0xLjA3NS0wLjAzNS0yLjA4Ny0wLjMyOS0yLjk3Mi0wLjgyMWMtMC4wMDEsMC4wMjctMC4wMDEsMC4wNTYtMC4wMDEsMC4wODIgIGMwLDMuMTgxLDIuMjYyLDUuODM0LDUuMjY1LDYuNDM3Yy0wLjU1LDAuMTQ5LTEuMTMsMC4yMy0xLjcyOSwwLjIzYy0wLjQyNCwwLTAuODM0LTAuMDQxLTEuMjM0LTAuMTE3ICBjMC44MzQsMi42MDYsMy4yNTksNC41MDQsNi4xMyw0LjU1OGMtMi4yNDUsMS43Ni01LjA3NSwyLjgxMS04LjE1LDIuODExYy0wLjUzLDAtMS4wNTMtMC4wMzEtMS41NjYtMC4wOTIgIEMyLjkwNSwyNy45MTMsNi4zNTUsMjksMTAuMDYyLDI5YzEyLjA3MiwwLDE4LjY3NS0xMC4wMDEsMTguNjc1LTE4LjY3NWMwLTAuMjg0LTAuMDA4LTAuNTY4LTAuMDItMC44NSAgQzMwLDguNTUsMzEuMTEyLDcuMzk1LDMxLjk5Myw2LjA3N3oiIGZpbGw9IiM1NUFDRUUiLz48Zy8%2BPGcvPjxnLz48Zy8%2BPGcvPjxnLz48L3N2Zz4%3D)](https://twitter.com/pyload)
[![Facebook](https://img.shields.io/badge/-facebook-3a589e.svg?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPD94bWwgdmVyc2lvbj0iMS4wIiA%2FPjwhRE9DVFlQRSBzdmcgIFBVQkxJQyAnLS8vVzNDLy9EVEQgU1ZHIDEuMC8vRU4nICAnaHR0cDovL3d3dy53My5vcmcvVFIvMjAwMS9SRUMtU1ZHLTIwMDEwOTA0L0RURC9zdmcxMC5kdGQnPjxzdmcgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgMzIgMzIiIGhlaWdodD0iMzJweCIgaWQ9IkxheWVyXzEiIHZlcnNpb249IjEuMCIgdmlld0JveD0iMCAwIDMyIDMyIiB3aWR0aD0iMzJweCIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI%2BPGc%2BPHBhdGggZD0iTTMyLDMwYzAsMS4xMDQtMC44OTYsMi0yLDJIMmMtMS4xMDQsMC0yLTAuODk2LTItMlYyYzAtMS4xMDQsMC44OTYtMiwyLTJoMjhjMS4xMDQsMCwyLDAuODk2LDIsMlYzMHoiIGZpbGw9IiMzQjU5OTgiLz48cGF0aCBkPSJNMjIsMzJWMjBoNGwxLTVoLTV2LTJjMC0yLDEuMDAyLTMsMy0zaDJWNWMtMSwwLTIuMjQsMC00LDBjLTMuNjc1LDAtNiwyLjg4MS02LDd2M2gtNHY1aDR2MTJIMjJ6IiBmaWxsPSIjRkZGRkZGIiBpZD0iZiIvPjwvZz48Zy8%2BPGcvPjxnLz48Zy8%2BPGcvPjxnLz48L3N2Zz4%3D)](https://www.facebook.com/pyload)
[![Join the chat](https://badges.gitter.im/pyload/webui.svg)](https://gitter.im/pyload/webui?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![IRC Freenode](https://img.shields.io/badge/irc-freenode-lightgray.svg)](https://kiwiirc.com/client/irc.freenode.com/#pyload)


Installation
------------

Type in your command shell **with _administrator/root_ privileges**:

    pip install pyload.webui[full]

Under Unix based systems this usually means you have to use `sudo`:

    sudo pip install pyload.webui[full]

The `full` option ensures that all the optional packages will downloaded and
installed as well as the mandatory ones.

You can install just the essential dependencies typing:

    pip install pyload.webui

If the above commands fail, consider using the
[`--user`](https://pip.pypa.io/en/latest/user_guide/#user-installs) option:

    pip install --user pyload.webui


------------------------------------------------------------------------------
###### © 2009-2015 pyLoad Team, © 2015-2017 Walter Purcaro <vuolter@gmail.com>
