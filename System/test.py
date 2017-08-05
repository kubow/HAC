# -*- coding: utf-8 -*-
import unittest

from log import Log # as Log2
from OS74 import Platform
from SO74 import OpenWeatherMap
from TX74 import WebContent, RssContent


class TestLog(unittest.TestCase):
    """Check if logging can process"""
    def test_simple_log(self):
        text = 'simple testing test'
        log_file = 'C:\\_Run\\Script\\Multimedia\\logfile.log'
        logger = Log(log_file, 'test', 'test.py', False)
        logger.log_operation(text)
        self.assertIn(text, logger.line_text)

    def test_advanced_log(self):
        text = 'advanced testing test'
        log_file = 'C:\\_Run\\Script\\Multimedia\\logfile.log'
        logger = Log(log_file, 'test', 'test.py', True)
        logger.log_operation(text)
        self.assertIn(text, logger.line_text)


class TestPlatform(unittest.TestCase):
    """Check for operating platform"""
    def test_platform(self):
        platform = Platform()
        print 'found platform'
        self.assertIn('win', platform.main)


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
        loc = 'file:///C:/_Run/Web/index.html'
        o = WebContent(loc)
        o.process_url()
        self.assertIn('encyklopedie', str(o.div))

    def test_web_content(self):
        loc = 'https://aktualnizpravy.cz/'
        o = WebContent(loc)
        o.process_url()
        self.assertIn('dnes m', str(o.div))


unittest.main()