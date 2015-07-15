# nibeuplink
Plugin for smarthome.py to retreive heatpump data from Nibe Uplink.
This plugin is based on scraping the webiste to show the data. This means that there are some limitations in the availability of data. Also, this means that in case of a change to the Nibe Uplink website the plugin might have to be updated.

## Configuration
### plugin.conf
<pre>
[nibeuplink]
    class_name = NibeUplink
    class_path = plugins.nibeuplink
    nibe_email = your.email@provider.com
    nibe_password = youruplinkpassword
    nibe_system = 12345 # your system id
</pre>

## Usage
You need to have a Nibe Uplink account for this plugin to work.
It is suggested to create a specific user for this plugin to avoid leaking your credentials, especially if you are using the remote management features for your heat pump(s)

The value for <pre>nibe_system</pre> can be seen when you are logged into NibeUplink. It's part of the URL when you open the service info page. I.e: https://www.nibeuplink.com/System/12345/Status/ServiceInfo

### items.conf
<pre>
['heatpump']
  [['outside_temperature']]
    type = num
    nibe_reg = ID40004
    sqlite = true
    visu_acl = true
</pre>

The <pre>nibe_reg</pre> parameter is the magical trick here. Here you specify the ID of the data register that you want to show. The Ids are identical to the modbus registers, i.e. described here: [nibebinding](https://github.com/openhab/openhab/wiki/Nibe-Heat-Pump-Binding#list-of-supported-modbus-coil-addresses-coiladdress)

The actual supported data points for your system can be retreived from the source code of the website. Just look for elements with classes in the format of IDxxxxx.

Here is a sample list of the values available from my F1245-6PC:

<pre>
ID40004
ID40067
ID40013
ID40014
ID43005
ID40022
ID40018
ID40019
ID40017
ID40015
ID40016
ID43416
ID43420
ID10012
ID43424
ID43439
ID43437
ID40008
ID40012
ID43009
ID40033
ID43161
ID40071
ID40008
ID40012
ID47276
ID44270
ID43152
ID10033
ID43081
ID43084
ID47212
ID47214
ID47411
ID47410
ID47409
ID47408
ID47407
ID47412
</pre>

## Open Issues
- There is no value casting for the time being. This means that more or less onyl numeric (float) values are supported.
- Not all values shown on the page have an ID and therefore can not be retreived. This might change in the future
