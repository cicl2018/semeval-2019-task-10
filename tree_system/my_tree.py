import json

class Node(object):
  def __init__(self, data=None, left_child=None, right_child=None):
    self.left = left_child
    self.right = right_child
    self.data = data

  def __repr__(self):
    dic = self.get_dict()
    return json.dumps(dic)

  def get_dict(self):
    data = {}
    data[self.data] = {}
    if self.left:
      # if there is left child
      if not self.left.left and not self.left.right: 
      # if left child only contains data, add data to representation
        data[self.data]['left_child'] = self.left.data
      else: 
      # if left child contains children, add representation of left child to main representation
        data[self.data]['left_child'] = self.left.get_dict()
    else: 
    # if there is no left child, add None to representation
      data[self.data]['left_child'] = None

    if self.right:
      # if there is right child
      if not self.right.left and not self.right.right:
      # if right child only contains data, add data to representation
        data[self.data]['right_child'] = self.right.data
      else:
      # if right child contains children, add representation of right child to main representation
        data[self.data]['right_child'] = self.right.get_dict()
    else:
    # if there is no right child, add None to representation
      data[self.data]['right_child'] = None

    return data

  def leaves_number(self):
    number = 0

    if self.left:
      number += self.left.leaves_number()
    if self.right:
      number += self.right.leaves_number()

    if not self.left and not self.right:
      number += 1

    return number

  def get_triples(self):
    arr_triples = []

    if self.left and self.right:
      if type(self.left.data) is dict and type(self.right.data) is dict:
        triple = {}
        triple["operation"] = self.data
        triple["q1"] = self.left.data
        triple["q2"] = self.right.data
        arr_triples.append(triple)
      else:
        arr_triples += self.left.get_triples()
        arr_triples += self.right.get_triples()

    return arr_triples

  def get_leaves(self):
    arr_leaves = []

    if self.left:
      arr_leaves += self.left.get_leaves()
    if self.right:
      arr_leaves += self.right.get_leaves()
    if not self.left and not self.right:
      arr_leaves += self.data

    return arr_leaves


  # def depth(self):
  #   left_depth = self.left.depth() if self.left else 0
  #   right_depth = self.right.depth() if self.right else 0
  #   return max(left_depth, right_depth) + 1

# printing out test tree
# n1 = Node(4)
# n2 = Node(8)
# n3 = Node(10)

# n4 = Node(None, n1, n2)
# n6 = Node(None, n3, n4)

# print(n6.leaves_number())