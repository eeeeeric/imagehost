imagehost
=========
upload to imagehosts from python

Install
-------
Requires `requests` and `beautifulsoup4`.

    python setup.py build
    python setup.py install

Usage
-----
```python
from imagehost.someimage import SomeImage
s = SomeImage(my_username, my_password)
images = [ 'test.png', 'test2.png' ]
html, bbcode, direct, gallery = s.upload(images, 
    thumb_size='w300', gallery_name='Test')
```

Supported ImageHosts
--------------------
- someimage.com
