import unittest
import xml.etree.ElementTree as ET
from io import StringIO
import sys
from parser import parse_xml, constants

class TestConfigConverter(unittest.TestCase):

    def test_comment_block(self):
        input_xml = '''<root>
            <comment>
                This is a comment.
                It spans multiple lines.
            </comment>
        </root>'''
        
        expected_output = '''{{!--
    This is a comment.
    It spans multiple lines.
--}}'''

        result = parse_xml(input_xml)
        self.assertEqual(result, expected_output)

    def test_constant_declaration(self):
        input_xml = '''<root>
            <constant name="MY_CONST">100</constant>
        </root>'''

        expected_output = 'var MY_CONST = 100'
        result = parse_xml(input_xml)
        self.assertEqual(result, expected_output)

    def test_array_declaration(self):
        input_xml = '''<root>
            <array name="myArray">
                <item>1</item>
                <item>2</item>
                <item>3</item>
            </array>
        </root>'''

        expected_output = 'var myArray = (1, 2, 3)'
        result = parse_xml(input_xml)
        self.assertEqual(result, expected_output)

    def test_evaluation(self):
        input_xml = '''<root>
            <evaluation name="myEval">someValue</evaluation>
        </root>'''

        expected_output = '![myEval]'
        result = parse_xml(input_xml)
        self.assertEqual(result, expected_output)

    def test_invalid_tag(self):
        input_xml = '''<root>
            <unknownTag>someValue</unknownTag>
        </root>'''

        expected_output = 'Неправильный синтаксис: unknownTag'
        result = parse_xml(input_xml)
        self.assertEqual(result, expected_output)

    def test_mixed_elements(self):
        input_xml = '''<root>
            <constant name="MY_CONST">100</constant>
            <comment>
                This is a comment.
            </comment>
            <array name="myArray">
                <item>1</item>
                <item>2</item>
            </array>
            <evaluation name="myEval">someValue</evaluation>
        </root>'''

        expected_output = '''var MY_CONST = 100
{{!--
    This is a comment.
--}}
var myArray = (1, 2)
![myEval]'''

        result = parse_xml(input_xml)
        self.assertEqual(result, expected_output)

    def test_empty_input(self):
        input_xml = '''<root></root>'''
        expected_output = ""
        result = parse_xml(input_xml)
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()