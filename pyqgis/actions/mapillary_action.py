import requests
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWebKitWidgets import QWebView
from qgis.utils import iface

# https://www.mapillary.com/developer/api-documentation#image

parameters = {
    'access_token': '<access token>',
    'bbox': '{},{},{},{}'.format([%$x%]-0.001,[%$y%]-0.001, [%$x%]+0.001, [%$y%]+0.001),
    'fields': 'thumb_1024_url',
	'limit': 1
}

response = requests.get(
        'https://graph.mapillary.com/images', params=parameters)
if response.status_code == 200:
    data_json = response.json()
    if data_json['data']:
        url = data_json['data'][0]['thumb_1024_url']
        myWV = QWebView(None)
        myWV.load(QUrl(url))
        myWV.show()
    else:
        qgis.utils.iface.messageBar().pushMessage('No images found')
