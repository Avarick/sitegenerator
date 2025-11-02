import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node_one = HTMLNode("p", "hello world")
        node_two = HTMLNode("p", "hello world")
        self.assertEqual(node_one, node_two)
    
    def test_noteq(self):
        node_one = HTMLNode("a", "hello world")
        node_two = HTMLNode("p", "hello world")
        self.assertNotEqual(node_one, node_two)

    def test_props(self):
        node = HTMLNode("a", None, None, {"href": "https://www.google.com",
                                        "target": "_blank",})
        print(node.props_to_html())
        return True