#!/usr/bin/env python3
#########################################################################
#  Copyright 2015 Sebastian Kuhn                  sebastian@derseppel.net
#########################################################################
#  This file is part of SmartHome.py.    http://mknx.github.io/smarthome/
#
#  SmartHome.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHome.py. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

from html.parser import HTMLParser
import re

try:
  from http.cookiejar import CookieJar
except ImportError:
  from cookielib import CookieJar


try:
  from urllib.parse import urlencode
  from urllib.request import build_opener
  from urllib.request import HTTPRedirectHandler
  from urllib.request import HTTPHandler
  from urllib.request import HTTPSHandler
  from urllib.request import HTTPCookieProcessor
except ImportError:
  import urllib2


class NibeHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.inSpan = False
    self.lasttag = None
    self.lastname = None
    self.lastvalue = None
    self.lastclass = None
    self.data = dict()
    self.regex_sz = re.compile(r'\\{1}[a-zA-Z\S]+')
    self.regex_perc = re.compile(r'%')
    self.regex_hours = re.compile(r'h$')
    self.regex_gm = re.compile(r'GM$')

  def handle_starttag(self, tag, attrs):
    self.inSpan = False
    self.lastclass = None
    if tag == 'span':
      for name, value in attrs:
        if name == 'class' and 'AutoUpdateValue' in value:
          self.inSpan = True
          self.lastclass = re.findall(r'ID\d{5}', value)[0]
          self.lasttag = tag

  def handle_endtag(self, tag):
    if tag == 'span':
      self.inSpan = False

  def handle_data(self, data):
    if self.lasttag == 'span' and self.inSpan and data.strip():
      strippedValue = re.sub(self.regex_sz, '', data)
      strippedValue = re.sub(self.regex_perc, '', strippedValue)
      strippedValue = re.sub(self.regex_hours, '', strippedValue)
      strippedValue = re.sub(self.regex_gm, '', strippedValue)
      self.data[self.lastclass] =  strippedValue

  def getDataArray(self):
    return self.data
