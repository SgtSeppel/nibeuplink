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

import logging
from datetime import datetime, timedelta

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
  from urllib.request import HTTPError
except ImportError:
  import urllib2


from .NibeHTMLParser import NibeHTMLParser

logger = logging.getLogger('')


class NibeUplink():
  def __init__(self, smarthome, nibe_email, nibe_password, nibe_system, nibe_update_cyle=10):
    logger.warn('Init NibeUplink')
    self._sh = smarthome
    self._items = dict()
    self.nibe_email = nibe_email
    self.nibe_password = nibe_password
    self.nibe_system = nibe_system
    self.nibe_update_cyle = nibe_update_cyle
    self.login_url = "https://www.nibeuplink.com/Login"
    self.service_url = "https://www.nibeuplink.com/System/"+self.nibe_system+"/Status/ServiceInfo"
    self.cookies = CookieJar()
    self.opener = None
    self.parser = None
    self.response = None
      
  def login(self):
   values = {'Email' : self.nibe_email,
          'Password' : self.nibe_password,
          'returnUrl' : ''
        }

   data = urlencode(values)
   binary_data = data.encode('ascii')

   self.opener = build_opener(
        HTTPRedirectHandler(),
        HTTPHandler(debuglevel=0),
        HTTPSHandler(debuglevel=0),
        HTTPCookieProcessor(self.cookies))

   self.response = self.opener.open(self.login_url, binary_data)

  def run(self):
    self.alive = True
    # Log into NibeUplink
    values = {'Email' : self.nibe_email,
          'Password' : self.nibe_password,
          'returnUrl' : ''
        }

    data = urlencode(values)
    binary_data = data.encode('ascii')
    
    self.opener = build_opener(
         HTTPRedirectHandler(),
         HTTPHandler(debuglevel=0),
         HTTPSHandler(debuglevel=0),
         HTTPCookieProcessor(self.cookies))
    
    self.parser = NibeHTMLParser()

    try:
      self.response = self.opener.open(self.login_url, binary_data)
    except HTTPError as e:
      logger.warn('Could not login')
    else:
      logger.warn('Logged in')
    
    self._sh.scheduler.add('NibeUplink', self._update_values, prio=5, cycle=self.nibe_update_cyle)

  def stop(self):
    self.alive = False

  def parse_item(self, item):
    if 'nibe_reg' in item.conf:
      self._items[item.conf['nibe_reg']] = item
    else:
      return None

  def update_item(self, item, caller=None, source=None, dest=None):
    logger.warn('NibeUplink: update_item():'+item)
    return None

  def _update_values(self):
    self.login()
    self.response = self.opener.open(self.service_url)
    page = self.response.read()
    self.parser.feed(str(page))
    tags = self.parser.getDataArray()
    for k,v in self._items.items():
      item = self._items[k]
      value = tags[k]
      try:
        item(float(value), 'NibeUplink')
      except:
        logger.warn('Problem Updating value: ' + k + ':' + tags[k])
      else:
        logger.debug('Updated value: ' + k + ':' + tags[k])
