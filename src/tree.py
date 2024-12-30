# 抽象语法树 基础结点类
class node:
    def __init__(self, key):
        self.key = str(key)

    def is_leaf(self):
        """判断是否为叶子结点（外部结点）"""
        return isinstance(self, exnode)

    def __repr__(self):
        return f"{self.__class__.__name__}(key={self.key})"


# 抽象语法树 内部结点类
# self.key {String}  符号类型
# self.children {List of internode or exnode}  子结点列表
class internode(node):
    def __init__(self, key, children):
        super().__init__(key)
        # 如果子结点不是 node 类型，将其转化为外部结点
        self.children = [
            child if isinstance(child, node) else exnode(str(child), str(child))
            for child in children
        ]

    def add_child(self, child):
        """向当前结点添加子结点"""
        if not isinstance(child, node):
            child = exnode(str(child), str(child))  # 将非 node 类型转化为外部结点
        self.children.append(child)

    def remove_child(self, child):
        """从当前结点移除指定子结点"""
        if child in self.children:
            self.children.remove(child)

    def __str__(self):
        return ' '.join(map(str, self.children))

    def traverse(self):
        """深度优先遍历整个子树，返回结点列表"""
        nodes = [self]
        for child in self.children:
            if isinstance(child, internode):
                nodes.extend(child.traverse())  # 递归遍历子结点
            else:
                nodes.append(child)
        return nodes

    def find_node(self, key):
        """根据结点的 key 查找结点"""
        if self.key == key:
            return self
        for child in self.children:
            if isinstance(child, internode):
                result = child.find_node(key)
                if result:
                    return result
            elif child.key == key:
                return child
        return None


# 抽象语法树 外部结点类
# self.key {String}  符号类型
# self.value {String}  终结符的值
class exnode(node):
    def __init__(self, key, value):
        super().__init__(key)
        self.value = str(value)

    def __str__(self):
        return self.value

    def get_value(self):
        """获取外部结点的值"""
        return self.value

    def set_value(self, new_value):
        """设置外部结点的值"""
        self.value = new_value
