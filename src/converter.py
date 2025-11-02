import textnode, htmlnode
import enum

class Converter():
    def text_node_to_html_node(text_node):
        if isinstance(text_node, textnode.TextNode):
            if text_node.text_type in {member for member in textnode.TextType}:
                if text_node.text_type == textnode.TextType.TEXT:
                    return htmlnode.LeafNode(None, text_node.text, None)
                elif text_node.text_type == textnode.TextType.BOLD:
                    return htmlnode.LeafNode("b", text_node.text, None)
                elif text_node.text_type == textnode.TextType.ITALIC:
                    return htmlnode.LeafNode("i", text_node.text, None)
                elif text_node.text_type == textnode.TextType.CODE:
                    return htmlnode.LeafNode("code", text_node.text, None)
                elif text_node.text_type == textnode.TextType.LINK:
                    return htmlnode.LeafNode("a", text_node.text, {"href": text_node.url,})
                elif text_node.text_type == textnode.TextType.IMAGE:
                    return htmlnode.LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
            else:
                raise Exception("Not a proper text type.")