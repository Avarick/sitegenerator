import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        if node.text_type != node2.text_type:
            return True
        else:
            return False

    def test_link(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://test.com/")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com/")
        if node.url != node2.url:
            return True
        else:
            return False
        
    def test_nourl(self):
        node = TextNode("This is a text node", TextType.BOLD, "http:/hi.com")
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()