class HTMLNode:
    
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):   
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        HTML_attributes = f""
        for attribute in self.props:
            HTML_attributes += f' {attribute}="{self.props[attribute]}"'
            
        return HTML_attributes
    
    def __eq__(self, node_two):
        if isinstance(node_two, HTMLNode):
            return self.tag == node_two.tag and self.value == node_two.value and self.children == node_two.children and self.props == node_two.props
        else:
            return False

    def __repr__(self):
        text_str = f"HTMLNode: TAG = {self.tag} | VALUE = {self.value} | CHILDREN = {self.children} | PROPS = {self.props}"
        return text_str

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        string = f""   
        if self.value is None:
            raise ValueError("There must be a value stated!")
        elif self.tag is None:
            string += f"{self.value}"
        else:
            string += f"<{self.tag}"
            if self.props is not None and len(self.props) > 0:
                string += f'{self.props_to_html()}'
            string += f">{self.value}</{self.tag}>"
        return string
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        string = f""
        if self.tag is None:
            raise ValueError("There must be a tag!")
        if self.children is None:
            raise ValueError("There must be children!")
        nested_string = f""
        for child in self.children:
            if isinstance(child, HTMLNode):
                nested_string += child.to_html()
        string += f"<{self.tag}"
        if self.props is not None and len(self.props) > 0:
            string += f'{self.props_to_html()}'
        if self.tag is "img":
            string += ">"
            return string
        string += f">{nested_string}</{self.tag}>"
        return string