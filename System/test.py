# -*- coding: utf-8 -*-
import unittest

from log import Log
from DV72 import ControlDevice
from OS74 import CurrentPlatform, FileSystemObject
from MP74 import OpenWeatherMap
from TX74 import WebContent, RssContent


def load_platform_based(from_path, web=None):
    base = FileSystemObject().dir_up(2)
    print(base)
    if web:
        return web + base + from_path
    else:
        return base + from_path

class DeviceSetting(unittest.TestCase):
    """Check if logging can process"""
    def test_device_basic(self):
        dev = ControlDevice()
        logger = Log(load_platform_based('Script/Multimedia/logfile.log'), 'Device', 'test.py', False)
        text = 'Checking device ({0}) setting: {1}'.format(dev.device_name, dev.setup_db)
        logger.log_operation(text)
        self.assertEquals(dev.interval_shift, 2)


class TestLocalContent(unittest.TestCase):
    """Check if local data accessible"""
    def test_local_content(self):
        location = 'C:\\_Run\\Script\\Multimedia'
        fso = FileSystemObject(location)
        logger = Log(load_platform_based('Script/Multimedia/logfile.log'), 'Folder', 'test.py', False)
        text = 'Checking folder ({0}) manageable: {1}'.format(location, str(1))
        logger.log_operation(text)
        self.assertEqual(fso.path, 'C:\\_Run\\Script\\Multimedia')


class TestWeather(unittest.TestCase):
    """Check if weather data accessible"""
    def test_weather(self):
        loc = 'Horni Pocernice,cz'  # 'Necin,cz'
        try:
            o = OpenWeatherMap(loc)
            text = 'Checking weather at location ({0}) manageable: {1}'.format(loc, o.heading[0])
        except:
            text = 'Cannot properly get {0} data : {1}'.format(loc, str(None))
        logger = Log(load_platform_based('Script/Multimedia/logfile.log'), 'Weather', 'test.py', False)
        logger.log_operation(text)
        self.assertIn(loc.split(',')[-1], o.heading[0])

    def test_dummy_weather(self):
        """Check if can treat no submitted location"""
        loc = ''  # 'Necin,cz'
        try:
            o = OpenWeatherMap(loc)
            text = 'Checking weather at location ({0}) manageable: {1}'.format(loc, o.heading[0])
        except:
            text = 'Cannot properly get {0} data : {1}'.format(loc, str(None))
        logger = Log(load_platform_based('Script/Multimedia/logfile.log'), 'Weather', 'test.py', False)
        
        logger.log_operation(text)
        self.assertIn(loc.split(',')[-1], o.heading[0])


class TestWebContent(unittest.TestCase):
    """Check if web data accessible"""
    def test_localhost_content(self):
        try:
            o = WebContent(load_platform_based('Web/index.html', 'file:///'))
            o.process_url()
            text = 'Checking Web Content of ({0}) : {1}'.format('index.html', o.url)
        except:
            text = 'Cannot properly get {0} from : {1}'.format('Web/index.html', o.url)
        logger = Log(load_platform_based('Script/Multimedia/logfile.log'), 'Webfile', 'test.py', False)
        logger.log_operation(text)
        self.assertIn('encyklopedie', str(o.div))

    def test_web_content(self):
        try:
            o = WebContent('https://aktualnizpravy.cz/')
            o.process_url()
            text = 'Check Web Content ({0}) : {1}'.format('index.html', o.url)
        except:
            text = 'Cannot properly get {0} from : {1}'.format('index.html', o.url)
        logger = Log(load_platform_based('Script/Multimedia/logfile.log'), 'Webfile', 'test.py', False)
        logger.log_operation(text)
        self.assertIn('dnes m', str(o.div))

    def test_rss_content(self):
        try:
            o = RssContent('http://www.root.cz/rss/clanky/')
        except:
            print('some bad happened')
        self.assertIn('root.cz', o.div)

unittest.main()
