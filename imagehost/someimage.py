import os

import requests
from bs4 import BeautifulSoup

from .ImageHost import ImageHost

class SomeImage(ImageHost):
    """Uploading class for someimage.com"""

    UPLOAD_URL  = 'http://someimage.com/upload.php'
    DONE_URL    = 'http://someimage.com/done'
    THUMB_SIZES = ['w100', 'w150', 'w200', 'w250', 'w300', 'w350',
                   'h100', 'h150', 'h200', 'h250', 'h300', 'h350']

    def __init__(self, username=None, password=None):
        super(SomeImage, self).__init__()
        self.username = username
        self.password = password
        self._session = requests.Session()
        self._soup    = None
        self._html    = None
        self._bbcode  = None
        self._direct  = None
        self._gallery = None
        # TODO: login if username and password are supplied

    def upload(self, images, safe=True, thumb_size='w200', gallery=True, 
               gallery_name='Gallery 1'):
        """Upload images to someimage.com

        Arguments:
        images       -- list of strings, contains paths to images for upload
        safe         -- bool, NSFW?
        thumb_size   -- one of the values in SomeImage.THUMB_SIZES, thumb sizes
                        are prefixed with the limiting dimension
        gallery      -- bool, create a gallery from images?
        gallery_name -- str, name of gallery

        Returns:
        (html, bbcode, direct, gallery) -- each are strings, or None
        html    -- html for images
        bbcode  -- bbcode for images
        direct  -- direct links to images
        gallery -- gallery link to images

        """
        data = { 
                    'safe'         : '1' if safe else '0',
                    'thumb'        : thumb_size,
                    'gallery'      : '1' if gallery else '0',
                    'galleryname'  : gallery_name
               }

        # TODO: Check HTTP response in case of error
        for image in images:
            filename        = os.path.basename(image)
            data['name']    = filename
            files           = { 'file' : open(image, 'rb') }
            self._session.post(SomeImage.UPLOAD_URL, data=data, files=files)

        self.result = self._session.get(SomeImage.DONE_URL)
        self.soup   = BeautifulSoup(self.result.text)

        self._html    = self._get_html()
        self._bbcode  = self._get_bbcode()
        self._direct  = self._get_direct()
        self._gallery = self._get_gallery(gallery and len(images) > 1)
        return self._html, self._bbcode, self._direct, self._gallery

    def _get_html(self):
        """Parse the soup for HTML links to images"""
        textareas = self.soup.find_all('textarea')
        if len(textareas):
            return textareas[0].text.strip()
        else:
            return self.soup.find_all('input', 
                { 'class' : 'viewlinkbox' })[0]['value']

    def _get_bbcode(self):
        """Parse the soup for BBCode links to images"""
        textareas = self.soup.find_all('textarea')
        if len(textareas) > 1:
            return textareas[1].text.strip()
        else:
            return self.soup.find_all('input', 
                { 'class' : 'viewlinkbox' })[1]['value']

    def _get_direct(self):
        """Parse the soup for direct links to images"""
        textareas = self.soup.find_all('textarea')
        if len(textareas) > 2:
            return self.soup.find_all('textarea')[2].text.strip().split('\n')
        else:
            return self.soup.find_all('input', 
                { 'class' : 'viewlinkbox' })[2]['value']

    def _get_gallery(self, gallery):
        """Parse the soup for a gallery link to images"""
        if gallery:
            text = self.soup.find('span', { 'class' : 'gallerylinkwhite' }).text
            return text.strip()[len('Gallery Link: '):]
        else:
            return self._direct
