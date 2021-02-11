"""
-------------------------------------------------------
Popularity Tree class.
-------------------------------------------------------
Author:  Andrei Secara
ID:      190232560
Email:   dbrown@wlu.ca
__updated__ = "2020-04-11"
-------------------------------------------------------
Linked class version of the Popularity_Tree (PT) ADT.
-------------------------------------------------------
"""
from copy import deepcopy


class _PT_Node:

    def __init__(self, value):
        """
        -------------------------------------------------------
        Initializes a PT node containing value. Child pointers
        are None, height is 1, count is 1
        Use: node = _PT_Node(value)
        -------------------------------------------------------
        Parameters:
            value - value for the node (?)
        Returns:
            A _PT_Node object (_PT_Node)
        -------------------------------------------------------
        """
        self._value = deepcopy(value)
        self._left = None
        self._right = None
        self._height = 1
        self._rcount = 1  # Retrieval count
        return

    def _update_height(self):
        """
        -------------------------------------------------------
        Updates the height of the current node. _height is 1 plus
        the maximum of the node's (up to) two child heights.
        Use: node._update_height()
        -------------------------------------------------------
        Returns:
            None
        -------------------------------------------------------
        """
        if self._left is None:
            left_height = 0
        else:
            left_height = self._left._height

        if self._right is None:
            right_height = 0
        else:
            right_height = self._right._height

        self._height = max(left_height, right_height) + 1
        return
    
    def __str__(self):
            """
            USE FOR TESTING ONLY
            -------------------------------------------------------
            Returns node height and value as a string - for debugging.
            -------------------------------------------------------
            """
            return "h: {}, v: {}".format(self._height, self._value)

class Popularity_Tree:

    def __init__(self):
        """
        -------------------------------------------------------
        Initializes an empty PT.
        Use: pt = PT()
        -------------------------------------------------------
        Returns:
            A PT object (PT)
        -------------------------------------------------------
        """
        self._root = None
        self._count = 0
        self._comparisons = 0
        return

    def is_empty(self):
        """
        -------------------------------------------------------
        Determines if pt is empty.
        Use: b = pt.is_empty()
        -------------------------------------------------------
        Returns:
            True if pt is empty, False otherwise.
        -------------------------------------------------------
        """
        return self._root is None

    def __len__(self):
        """
        -------------------------------------------------------
        Returns the number of nodes in the PT.
        Use: n = len(pt)
        -------------------------------------------------------
        Returns:
            the number of nodes in pt.
        -------------------------------------------------------
        """
        return self._count
    
    def __contains__(self, key):
        """
        ---------------------------------------------------------
        Determines if the Popularity_Tree contains key.
        Use: b = key in pt
        -------------------------------------------------------
        Parameters:
          key - a comparable data element (?)
        Returns:
          Returns True if pt contains key, False otherwise.
        -------------------------------------------------------
        """
        value = self.retrieve(key)
        return value is not None

    def height(self):
        """
        -------------------------------------------------------
        Returns the maximum height of a PT, i.e. the length of the
        longest path from root to a leaf node in the tree.
        Use: h = pt.height()
        -------------------------------------------------------
        Returns:
            h - maximum height of pt (int)
        -------------------------------------------------------
        """
        if self._root is None:
            h = 0
        else:
            h = self._root._height
        return h

    def insert(self, value):
        """
        -------------------------------------------------------
        Inserts a copy of value into pt. Values may appear
        only once in a tree.
        Use: b = pt.insert(value)
        -------------------------------------------------------
        Parameters:
            value - data to be inserted into pt (?)
        Returns:
            inserted - True if value is inserted into pt,
                False otherwise. (boolean)
        -------------------------------------------------------
        """
        self._root, inserted = self._insert_aux(self._root, value)
        return inserted

    def _insert_aux(self, node, value):
        """
        -------------------------------------------------------
        Inserts a copy of _value into node.
        Private recursive operation called only by insert.
        Use: node, inserted = self._insert_aux(node, value)
        -------------------------------------------------------
        Parameters:
            node - a PT node (_PT_Node)
            value - data to be inserted into the node (?)
        Returns:
            node - the current node (_PT_Node)
            inserted - True if value is inserted into node,
                False otherwise. (boolean)
        -------------------------------------------------------
        """
        if node is None:
            # Base case: add a new node containing the value.
            node = _PT_Node(value)
            self._count += 1
            inserted = True
        elif value < node._value:
            # General case: check the left subtree.
            node._left, inserted = self._insert_aux(node._left, value)
        elif value > node._value:
            # General case: check the right subtree.
            node._right, inserted = self._insert_aux(node._right, value)
        else:
            # Base case: value is already in the PT.
            inserted = False

        if inserted:
            # Update the node height if any of its children have been changed.
            node._update_height()
        return node, inserted
    
    def retrieve(self, key):
        """
        -------------------------------------------------------
        Retrieves a copy of a value matching key in a BST. (Iterative)
        Use: v = bst.retrieve(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            returns
            value - value in the node containing key, otherwise None (?)
        -------------------------------------------------------
        """
        node = self._root
        value = None

        while node is not None and value is None:

            if node._value > key:
                node = node._left
            elif node._value < key:
                node = node._right
            elif node._value == key:
                # for comparison counting
                value = deepcopy(node._value)
        if value is not None:
            node._rcount += 1
        return value
    
    
    def retrieve_r(self, key):
        """
        -------------------------------------------------------
        Retrieves a copy of a value matching key in pt.
        Updates the node _rcount and reorders the nodes if their
        priorities require it.
        Use: v = pt.retrieve(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            value - value in the node containing key, otherwise None (?)
        -------------------------------------------------------
        """
        node, value = self._retrieve_aux(self._root, key)
        if value is not None:
            node._rcount += 1
            
        return value

    def _retrieve_aux(self, node, key):
        """
        -------------------------------------------------------
        Extracts a copy of _value from node if _value matches key.
        Update _rcount if key found. Rotates node if necessary.
        Private recursive operation called only by retrieve.
        Use: node, value = self._retrieve_aux(node, key)
        -------------------------------------------------------
        Parameters:
            node - a pt node (_PT_Node)
            key - data to search for (?)
        Returns:
            node - the current node (_PT_Node)
            value - copy of _value matching key, otherwise None (?)
        -------------------------------------------------------
        """
        
        if node is None:
            value = None
        else:
            if key < node._value:
                node, value = self._retrieve_aux(node._left, key)
                
                if node._left is not None:
                    if node._rcount < node._left._rcount:
                        node = self._rotate_right(node)
                node._update_height()
                
                
            elif key > node._value:
                node, value = self._retrieve_aux(node._right, key)
                
                if node._right is not None:
                    if node._rcount < node._right._rcount:
                        node = self._rotate_left(node)
                node._update_height()
            else:
                value = deepcopy(node._value)
        return node, value


    def _rotate_left(self, parent):
        """
        -------------------------------------------------------
        Rotates the parent node to its left around its right child.
        Updates the heights of the rotated nodes.
        Use: parent = self._rotate_left(parent)
        -------------------------------------------------------
        Parameters:
            parent - the pivot node to rotate around (_PT_Node)
        Returns:
            updated - the node with the updated _rcount that replaces
                the parent node (_PT_Node)
        -------------------------------------------------------
        """
        tempnode = parent._right
        parent._right = tempnode._left
        tempnode._left = parent
        parent._update_height()
        return tempnode
        

    def _rotate_right(self, parent):
        """
        -------------------------------------------------------
        Rotates the parent node to its right around its left child.
        Updates the heights of the rotated nodes.
        Use: parent = self._rotate_right(parent)
        -------------------------------------------------------
        Parameters:
            parent - the pivot node to rotate around (_PT_Node)
        Returns:
            updated - the node with the updated _rcount that replaces
                the parent node (_PT_Node)
        -------------------------------------------------------
        """
        tempnode = parent._left
        parent._left = tempnode._right
        tempnode._right = parent
        parent._update_height()
        return tempnode

    def inorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in inorder order.
        Use: a = pt.inorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in inorder (list of ?)
        -------------------------------------------------------
        """
        a = []
        self._inorder_aux(self._root, a)
        return a

    def _inorder_aux(self, node, a):
        """
        ---------------------------------------------------------
        Traverses node subtree in inorder. a contains the contents of
        node and its children in inorder.
        Private recursive operation called only by inorder.
        Use: self._inorder_aux(node, a)
        ---------------------------------------------------------
        Parameters:
            node - an PT node (_PT_Node)
            a - target list of data (list of ?)
        Returns:
            None
        ---------------------------------------------------------
        """
        if node is not None:
            self._inorder_aux(node._left, a)
            a.append(deepcopy(node._value))
            self._inorder_aux(node._right, a)
        return

    def preorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in preorder order.
        Use: a = pt.preorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in preorder (list of ?)
        -------------------------------------------------------
        """
        a = []
        self._preorder_aux(self._root, a)
        return a

    def _preorder_aux(self, node, a):
        """
        ---------------------------------------------------------
        Traverses node subtree in preorder. a contains the contents of
        node and its children in preorder.
        Private recursive operation called only by preorder.
        Use: self._preorder_aux(node, a)
        ---------------------------------------------------------
        Parameters:
            node - an PT node (_PT_Node)
            a - target of data (list of ?)
        Returns:
            None
        ---------------------------------------------------------
        """
        if node is not None:
            a.append(deepcopy(node._value))
            self._preorder_aux(node._left, a)
            self._preorder_aux(node._right, a)
        return

    def postorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in postorder order.
        Use: a = pt.postorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in postorder (list of ?)
        -------------------------------------------------------
        """
        a = []
        self._postorder_aux(self._root, a)
        return a

    def _postorder_aux(self, node, a):
        """
        ---------------------------------------------------------
        Traverses node subtree in postorder. a contains the contents of
        node and its children in postorder.
        Private recursive operation called only by postorder.
        Use: self._postorder_aux(node, a)
        ---------------------------------------------------------
        Parameters:
            node - an PT node (_PT_Node)
            a - target of data (list of ?)
        Returns:
            None
        ---------------------------------------------------------
        """
        if node is not None:
            self._postorder_aux(node._left, a)
            self._postorder_aux(node._right, a)
            a.append(deepcopy(node._value))
        return

    def levelorder(self):
        """
        -------------------------------------------------------
        Copies the contents of the tree nodes in levelorder order to a list.
        Use: values = pt.levelorder()
        -------------------------------------------------------
        Returns:
            nodes - a list containing the nodes of pt in levelorder.
            (list of _PT_Node)
        -------------------------------------------------------
        """
#         nodes = []
# 
#         if self._root is not None:
#             # Put the nodes for one level into a queue.
#             queue = []
#             queue.append(self._root)
# 
#             while len(queue) > 0:
#                 # Add a copy of the data to the sublist
#                 node = queue.pop(0)
#                 nodes.append(deepcopy(node))
# 
#                 if node._left is not None:
#                     queue.append(node._left)
#                 if node._right is not None:
#                     queue.append(node._right)
#         return nodes
        if self._root is not None:
            # Put the nodes for one level into a list.
            this_level = list()
            this_level.append(self._root)

            while this_level != []:
                # Create a list for the children of this node.
                next_level = list()

                for node in this_level:
                    print(node._value, end=',')

                    if node._left is not None:
                        next_level.append(node._left)
                    if node._right is not None:
                        next_level.append(node._right)
                print()
                # Process the next level.
                this_level = next_level
        return
    
    
    def _node_height(self, node):
        """
        ---------------------------------------------------------
        Helper function to determine the height of node - handles empty node.
        Private operation called only by _is_valid_aux.
        Use: h = self._node_height(node)
        ---------------------------------------------------------
        Parameters:
            node - the node to get the height of (_BST_Node)
        Returns:
            height - 0 if node is None, node._height otherwise (int)
        ---------------------------------------------------------
        """
        if node is None:
            height = 0
        else:
            height = node._height
        return height
    
    
    def is_valid(self):
        """
        ---------------------------------------------------------
        Determines if pt is valid.
        Use: b = pt.is_valid()
        ---------------------------------------------------------
        Returns:
            valid - True if the tree is a PT, False otherwise (boolean)
        ---------------------------------------------------------
        """
        valid = self._is_valid_aux(self._root)
        return valid

    def _is_valid_aux(self, node):
        """
        ---------------------------------------------------------
        Helper function to determine the Popularity_Tree validity of node.
        Private operation called only by is_valid.
        Use: b = self._is_valid_aux(node)
        ---------------------------------------------------------
        Parameters:
            node - the node to check the validity of (_PT_Node)
        Returns:
            result - True if node is a Popularity_Tree, False otherwise (boolean)
        ---------------------------------------------------------
        """
        '''
        valid = True
        if node._left is not None:
            valid = valid and self._is_valid_aux(node._left)
            valid = valid and node._left._value <= node._value

        if node._right is not None:
            valid = valid and self._is_valid_aux(node._right)
            valid = valid and node._right._value <= node._value

        return valid
        '''
                                        
        if node is None:
            valid = True
        elif (node._left is not None and node._left._rcount > node._rcount) or (node._right is not None and node._right._rcount > node._rcount):
            valid = False
        elif (node._left is not None and node._left._value > node._value) or (node._right is not None and node._right._value < node._value):
            valid = False
        elif node._height != max(self._node_height(node._left), self._node_height(node._right)) + 1:
            valid = False
        else:
            valid = self._is_valid_aux(node._left) and self._is_valid_aux(node._right)
        return valid
