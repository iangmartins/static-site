class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        f_string = ""
        if not self.props:
            return f_string

        for key in self.props:
            f_string += " "
            f_string += f'{key}="{self.props[key]}"'
        
        return f_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaves MUST have a value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("ERROR: TAG missing")
        if self.children == None:
            raise ValueError("ERROR: CHILDREN missing")
        html = ""
        for child in self.children:
            html += child.to_html()
        return f'<{self.tag}>{html}</{self.tag}>'