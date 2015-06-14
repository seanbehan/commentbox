import os
import app
import unittest
import tempfile
from flask import json, jsonify

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def test_home(self):
        rv = self.app.get('/')
        assert 'Welcome' in rv.data

    def test_places_api(self):
        data = json.loads(self.app.get('/places.json').data)
        assert len(data)==2


if __name__ == '__main__':
    unittest.main()
