from my_tree import Node

def add_leaf(tree, node):
	yield(Node(None, node, tree))
	if tree.left and tree.right:
		for left in add_leaf(tree.left, node):
			yield Node(None, left, tree.right)
		for right in add_leaf(tree.right, node):
			yield Node(None, tree.left, right)

# together with add_leaf, provides an enumeration of all binary trees with given labels
def enum_unordered(labels):
	if len(labels) == 1:
		yield Node(labels[0])
	else:
		for tree in enum_unordered(labels[1:]):
			for new_tree in add_leaf(tree, Node(labels[0])):
				yield new_tree

# printing all binary trees for quantities (4, 8, 10)
# arr = [4, 8, 10]
# all_trees = []
# for tree in enum_unordered((4, 8, 10)):
# 	all_trees.append(tree)
# 	print(tree)
# print(len(all_trees))

# assigns operations for tree nodes, provides all possible enumerations
def operations_for_nodes(tree, ifReverse):
	# set of operations
	if ifReverse:
		operations = ["+", "-", "-rev", "x", "/", "/rev"]
	else:
		operations = ["+", "-", "x", "/"]
	# if node is "empty", choose an operation
	if tree.data == None:
		for operation in operations:
			# if left child's value is None, choose operations to it
			if tree.left.data == None:
				# variants of left child (for every value of node)
				for left_child in operations_for_nodes(tree.left, ifReverse):
					# right child's value is None, choose operations to it
					if tree.right.data == None:
						# variants of right child (for every value of node and of left child)
						for right_child in operations_for_nodes(tree.right, ifReverse):
							# combine together operation for node, variant of left child and variant of right child
							yield Node(operation, left_child, right_child)
					# if right child doesn't exist or its value is not None, do not change right part of tree
					else:
						# combine together operation for node, variant of left child and right child of tree
						yield Node(operation, left_child, tree.right)
			# if right child's value is None (but left child's value is not None), choose operations for right child's value
			elif tree.right.data == None:
				# variants of right child (for every value of node)
				for right_child in operations_for_nodes(tree.right, ifReverse):
					# combine together operation for node, left child of tree and variant of right child
					yield Node(operation, tree.left, right_child)
			# if node is a leaf (both left child and right child have values different from None), do not change left or right part of tree
			elif tree.left.data != None and tree.right.data != None:
				# combine together operation for node, left child of tree and right child of tree
				yield Node(operation, tree.left, tree.right)
		# tree.data = None

# fill internal nodes with operation signs and check if trees add to array
# n1 = Node(4)
# n2 = Node(8)
# n3 = Node(10)

# n5 = Node(None, n1, n2)
# n6 = Node(None, n5, n3)

# trees = []
# for tree in operations_for_nodes(n6):
	# print(tree)
	# trees.append(tree)
# print(trees[0:4])
# for tree in trees:
# 	print(tree)

# perform the operation in the node data on two of its leaves-children (quantities)
def calculate_node(node, ifReverse):
	operation = node.data
	left_data = node.left.data
	right_data = node.right.data
	if left_data != None and right_data != None:
		if type(left_data) is dict:
			left_data = left_data["value"]
		if type(right_data) is dict:
			right_data = right_data["value"]

		if operation == "+":
			return (left_data + right_data)
		elif operation == "-":
			return (left_data - right_data)
		elif operation == "x":
			return (left_data * right_data)
		elif operation == "/" and right_data != 0.0:
			return (left_data / right_data)
		if ifReverse:
			if operation == "-rev":
				return (right_data - left_data)
			elif operation == "/rev" and left_data != 0.0:
				return (right_data / left_data)
	return None

# calculate the outcome of tree based on nodes filled with operations
def calculate_tree(tree, ifReverse):
	if ifReverse:
		operations = ["+", "-", "-rev", "x", "/", "/rev"]
	else:
		operations = ["+", "-", "x", "/"]

	# if children of node are leaves, use calculate_node to perform the operation on them
	if (tree.left.data not in operations) and (tree.right.data not in operations):
		return calculate_node(tree, ifReverse)

	# if a child or both children of node aren't leaves, calculate left and right part separately, 
	# and use the results to perform the operation in the node
	else:
		if tree.left.data in operations:
			left_component = calculate_tree(tree.left, ifReverse)
		else:
			left_component = tree.left.data

		if tree.right.data in operations:
			right_component = calculate_tree(tree.right, ifReverse)
		else:
			right_component = tree.right.data

		return calculate_node(Node(tree.data, Node(left_component), Node(right_component)), ifReverse)

# n1 = Node(4)
# n2 = Node(8)
# n3 = Node(10)

# n5 = Node("+", n1, n2)
# n6 = Node("+", n5, n3)

# print(calculate_tree(n6))

# check if tree is monotomic based on two constraints
def check_monotomic(tree, ifReverse):
	if ifReverse:
		operations = ["+", "-", "-rev", "x", "/", "/rev"]
	else:
		operations = ["+", "-", "x", "/"]

	# if node is leaf node (quantity)
	if tree.data not in operations:
		return True
	# checking constraint #1: If an addition node is connected to a subtraction node, then the subtraction node is the parent
	if tree.data == "+":
		if tree.left.data == "-" or tree.right.data == "-":
			return False
		if ifReverse:
			if tree.left.data == "-rev" or tree.right.data == "-rev":
				return False
	# checking constraint #2: If a multiplication node is connected to a division node, then the division node is the parent
	if tree.data == "x":
		if tree.left.data == "/" or tree.right.data == "/":
			return False
		if ifReverse:
			if tree.left.data == "/rev" or tree.right.data == "/rev":
				return False

	# if check gets to this point, recursively apply the function to left and right children of the node
	left_check = check_monotomic(tree.left, ifReverse)
	right_check = check_monotomic(tree.right, ifReverse)
	return (left_check and right_check)

# n1 = Node(4)
# n2 = Node(8)
# n3 = Node(10)
# n4 = Node(5)

# n5 = Node("/", n1, n2)
# n6 = Node("x", n3, n4)
# tree = Node("/", n5, n6)

# print(check_monotomic(tree))