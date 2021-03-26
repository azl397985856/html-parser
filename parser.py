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


def extract_attrs(text):
    attrs = dict()
    for x in text.split()[1:]:
        k, v = x.split("=")
        attrs[k] = v[1:-1]  # trim quotes
    return attrs


def is_self_close(tagName):
    # your can also add more self_close tags into this list
    return tagName.upper() in ["BR", "IMG"]


class HTMLParser:
    def __init__(self, html):
        self.html = html
        self.pending = []

    def pop_pendings(self):
        node = self.pending.pop()
        # since we keep track with a stack data structure
        # so the very last popped node is the root of dom
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
        tagName = tag.split()[0]
        if tag.startswith("/"):
            if len(self.pending) == 1:
                return
            # close tag. just finish this tag by poping stack out
            node = self.pending.pop()
            parent = self.pending[-1]
            parent.children.append(node)
        elif is_self_close(tagName):
            parent = self.pending[-1]
            node = Element(tagName, parent)
            node.attrs = extract_attrs(tag[:-1])
            parent.children.append(node)
        else:
            # open tag. similar with add_text, the difference is that: at this case, we only  append node to unfinish, not the parent node
            parent = self.pending[-1] if self.pending else None  # the very first element has no parent, we use keyword None to track this case
            node = Element(tagName, parent)
            node.attrs = extract_attrs(tag)
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
        if is_self_close(node.tagName):
            print(" " * depth * TAB_SIZE, "<" + node.tagName + " " + " ".join([k + "='" + v + "'" for k, v in node.attrs.items()]) + "/>")
        else:
            print(" " * depth * TAB_SIZE, "<" + node.tagName + " " + " ".join([k + "='" + v + "'" for k, v in node.attrs.items()]) + ">")
    for child in node.children:
        print_tree(child, depth + 1)
    if isinstance(node, Element):
        if not is_self_close(node.tagName):
            print(" " * depth * TAB_SIZE, "</" + node.tagName + ">")


html = "<html><head></head><body><div class='lucifer' id='root'><br /><h1>This is my webpage</h1> <img src='https://tva1.sinaimg.cn/large/008eGmZEly1goxaieaddyj313e0u00v0.jpg' /></div></body></html>"

root = HTMLParser(html).parse()
print_tree(root)
