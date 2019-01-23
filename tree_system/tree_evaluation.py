from keras.models import load_model
import relevance_classifier as rel
import ancestor_classifier as anc
from sklearn.preprocessing import OneHotEncoder


def evaluate_trees(possible_trees, relevances, ancestors, categories):
    tree_ratings = {}
    for id in possible_trees.keys():
        for tree in possible_trees[id]:
            quantities = []
            quantity_pairs_ancestors = []
            #get the quantities and lowest common ancestor for each quantity pair

            #classifier data for the tree
            tree_relevances = relevances[id]
            tree_ancestors = ancestors[id]
            relevance_rating = 1
            ancestor_rating = 1

            #rate the tree for relevance and ancestor nodes
            for quantity in quantities:
                relevance_rating *= tree_relevances[quantity]
            for pair in quantity_pairs_ancestors.keys():
                ancestor = pair[1]
                index = categories.index(ancestor)
                probability_of_ancestor = tree_ancestors[pair][index]
                ancestor_rating *= probability_of_ancestor
            tree_rating = relevance_rating + ancestor_rating
            if id not in tree_ratings:
                tree_ratings[id] = [(tree, tree_rating)]
            else:
                tree_ratings[id].append((tree, tree_rating))

    return tree_ratings


if __name__ == "__main__":
    #get relevance ratings
    mlp_relevances = load_model('relevance_mlp.h5')
    x, y, quantities, ids = rel.preprocess('dummy_table_relevance.csv')
    relevances = rel.predict_relevances(mlp_relevances, x, quantities, ids)

    #get most likely common ancestor ratings
    mlp_ancestors = load_model('ancestor_mlp.h5')
    x, y, operations, anc_quantities, ids = anc.preprocess('dummy_table_ancestor.csv')
    y_enc = OneHotEncoder(sparse=False)
    y_enc.fit(y)
    y = y_enc.transform(y)
    categories = list(y_enc.categories_[0])
    print(categories.index('+'))
    ancestors, categories = anc.predict_operations(mlp_ancestors, x, quantities, ids, categories)



