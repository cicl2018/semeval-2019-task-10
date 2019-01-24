from keras.models import load_model
import relevance_classifier as rel
import ancestor_classifier as anc
from all_possible_trees import all_trees_for_all_questions
from my_tree import Node
from sklearn.preprocessing import OneHotEncoder


def evaluate_trees(possible_trees, relevances, ancestors, categories):
    tree_ratings = {}
    for id in possible_trees.keys():
       # print(tree_ratings)
        if id not in ancestors.keys():
            continue
        tree_ratings[id] = []
        for tree in possible_trees[id]:
            #quantities = Node.get_leaves(tree)
            quantity_pairs_ancestors = Node.get_triples(tree)
            #get the quantities and lowest common ancestor for each quantity pair

            #classifier data for the tree
           # tree_relevances = relevances[id]
            tree_ancestors = ancestors[id]
            relevance_rating = 1
            ancestor_rating = 1

            #rate the tree for relevance and ancestor nodes
            #for quantity in quantities:
            #    print(quantity)
             #   relevance_rating *= tree_relevances[quantity['value']]
            for pair in quantity_pairs_ancestors:
                ancestor = pair['operation']
                q1 = str(pair['q1']['value'])
                q2 = str(pair['q2']['value'])
                if (q1, q2) not in tree_ancestors.keys():
                    continue
                index = categories.index(ancestor)
                probability_of_ancestor = tree_ancestors[(q1, q2)][index]
                ancestor_rating *= probability_of_ancestor
            tree_rating = 1000 * ancestor_rating # + relevance_rating
            tree_ratings[id].append((tree, tree_rating))

    return tree_ratings


if __name__ == "__main__":
    #get relevance ratings
    #mlp_relevances = load_model('relevance_mlp.h5')
   # x, y, quantities, ids = [], [], [], [] #rel.preprocess('dummy_table_relevance.csv')
    relevances = []#rel.predict_relevances(mlp_relevances, x, quantities, ids)

    #get most likely common ancestor ratings
    mlp_ancestors = load_model('ancestor_mlp.h5')
    x, y, operations, anc_quantities, ids = anc.preprocess('lca.csv')
    y_enc = OneHotEncoder(sparse=False)
    y_enc.fit(y)
    y = y_enc.transform(y)
    categories = list(y_enc.categories_[0])
    ancestors, categories = anc.predict_operations(mlp_ancestors, x, anc_quantities, ids, categories)
    possible_trees = all_trees_for_all_questions('answered_questions_new.json')
    ratings = evaluate_trees(possible_trees, relevances, ancestors, categories)



