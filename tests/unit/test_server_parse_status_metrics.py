import unittest

from collections import namedtuple
from prometheus_client.core import GaugeMetricFamily
import xml.etree.ElementTree as ET

from tableau_exporter.server_parser_status_metrics import TableauServerStatusParser

class TestTableauServerStatusParser(unittest.TestCase):
    DEFAULT_MACHINE_NAME='test'
    DEFAULT_PROCESS_NAME='testprocess'
    DEFAULT_STATUS='ActiveSyncing'
    DEFAULT_XML='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <systeminfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <machines>
                        <machine name="{}">
                            <{} worker="test" status="{}"/>
                        </machine>
                    </machines>
                </systeminfo>'''

    @staticmethod
    def init_default_check(
        machine_name=DEFAULT_MACHINE_NAME,
        process_name=DEFAULT_PROCESS_NAME,
        status=DEFAULT_STATUS,
        xml=DEFAULT_XML
    ):
        """Initialize a xml object for given status."""
        xml_response = xml.format(machine_name,process_name,status)
        xml_response = ET.fromstring(xml_response)
        return xml_response

    def test_tableau_server_parse_status_metrics(self):
        """Test creation of a prometheus metric from server status"""
        xml_response = TestTableauServerStatusParser.init_default_check()
        got = TableauServerStatusParser.tableau_server_parse_status_metrics(xml_response=xml_response[0])
        print got.name
        expected = 'tableau_server_process_status'
        print expected
        self.assertEqual(expected, got.name)
