class Node:
    def __init__(self, parent):
        self.parent = parent
        self.children = []


class Text(Node):
    def __init__(self, text, parent):
        Node.__init__(self, parent)  # inherit
        self.text = text


class Element(Node):
    def __init__(self, tagName, parent):
        Node.__init__(self, parent)
        self.tagName = tagName


class HTMLParser:
    def __init__(self, html):
        self.html = html
        self.pending = []

    def pop_pendings(self):
        node = self.pending.pop()
        if not self.pending:
            return node
        parent = self.pending[-1]
        parent.children.append(node)
        self.pop_pendings()

    def add_text(self, text):
        parent = self.pending[-1]
        node = Text(text, parent)
        parent.children.append(node)

    def add_tag(self, tag):
        if tag.startswith("/"):
            if len(self.pending) == 1:
                return
            # close tag. just finish this tag by poping stack out
            node = self.pending.pop()
            parent = self.pending[-1]
            parent.children.append(node)
        else:
            # open tag. similar with add_text, the difference is that: at this case, we only  append node to unfinish, not the parent node
            parent = self.pending[-1] if self.pending else None
            node = Element(tag, parent)
            self.pending.append(node)

    def parse(self):
        text = ""
        inside = False

        for c in self.html:
            if c == "<":
                inside = True
                if text:
                    self.add_text(text)  # eg: <div>hello <span>world!</span></div>
                text = ""
            elif c == ">":
                inside = False
                self.add_tag(text)
                text = ""
            else:
                text += c

        return self.pop_pendings()


TAB_SIZE = 4


def print_tree(node, depth=0):
    if isinstance(node, Text):
        print(" " * depth * TAB_SIZE, node.text)
    else:
        print(" " * depth * TAB_SIZE, "<" + node.tagName + ">")
    for child in node.children:
        print_tree(child, depth + 1)
    if isinstance(node, Element):
        print(" " * depth * TAB_SIZE, "</" + node.tagName + ">")


html = "<html><head></head><body><h1>This is my webpage</h1></body></html>"

nodes = HTMLParser(html).parse()
print_tree(nodes)
