# -*- coding: utf-8 -*-
import unittest

from log import Log
from DV72 import Device
from OS74 import CurrentPlatform, FileSystemObject
from SO74MP import OpenWeatherMap
from SO74TX import WebContent, RssContent


def load_platform_based(from_path, web=None):
    plf = CurrentPlatform()
    if 'win' == plf.main:
        if web:
            return web + 'C:\\_Run\\' + from_path
        else:
            return 'C:\\_Run\\' + from_path
    elif 'lnx' == plf.main or 'linux' == plf.main:
        if web:
            return web + '/home/kubow/Dokumenty/' + from_path
        else:
            return '/home/kubow/Dokumenty/' + from_path
    else:
        return None


class DeviceSetting(unittest.TestCase):
    """Check if logging can process"""
    def test_device_basic(self):
        dev = Device()
        logger = Log(load_platform_based('Script/Multimedia/logfile.log'), 'Device', 'test.py', False)
        text = 'Checking device ({0}) setting: {1}'.format(dev.device_name, dev.setup_db)
        logger.log_operation(text)
        self.assertEquals(dev.interval_shift, 2)


class TestLocalContent(unittest.TestCase):
    """Check if local data accessible"""
    def test_local_content(self):
        file_path = 'C:\\_Run\\Script\\Multimedia'
        fso = FileSystemObject(file_path)
        self.assertEqual(fso.path, file_path)


class TestWeather(unittest.TestCase):
    """Check if weather data accessible"""
    def test_weather(self):
        loc = 'Horni Pocernice,cz'  # 'Necin,cz'
        o = OpenWeatherMap(loc)
        self.assertIn(loc.split(',')[-1], o.heading[0])

    def test_dummy_weather(self):
        """Check if can treat no submitted location"""
        loc = ''  # 'Necin,cz'
        o = OpenWeatherMap(loc)
        self.assertIn(loc.split(',')[-1], o.heading[0])





class TestWebContent(unittest.TestCase):
    """Check if weather data accessible"""
    def test_localhost_content(self):
        loc = load_platform_based('Web/index.html', 'file:///')
        o = WebContent(loc)
        o.process_url()
        self.assertIn('encyklopedie', str(o.div))

    def test_web_content(self):
        loc = 'https://aktualnizpravy.cz/'
        o = WebContent(loc)
        o.process_url()
        self.assertIn('dnes m', str(o.div))

    def test_rss_content(self):
        loc = 'https://aktualnizpravy.cz/'
        o = WebContent(loc)
        o.process_url()
        self.assertIn('dnes m', str(o.div))

unittest.main()
