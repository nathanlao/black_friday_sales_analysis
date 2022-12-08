import sys
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def MLClassifiers(data, f):

    # map/convert string values to a numeric number
    mapping_age = {'0-17': 0, '18-25': 1, '26-35': 2, '36-45': 3, '46-50': 4,
                   '51-55': 5, '55+': 6}
    mapping_gender = {'F': 0, 'M': 1}
    mapping_city = {'A': 0, 'B': 1, 'C': 2}
    mapping_stay_in_city_years = {'4+': 4}
    data = data.replace({'Age': mapping_age,
                         'Gender': mapping_gender,
                         'City_Category': mapping_city,
                         'Stay_In_Current_City_Years': mapping_stay_in_city_years})

    # Nah value in product category 2 and 3, but we are still interested in them
    data['Product_Category_2'] = data['Product_Category_2'].fillna(0).astype(
        'int64')
    data['Product_Category_3'] = data['Product_Category_3'].fillna(0).astype(
        'int64')

    # Have 9 features for our classification problem
    data = data.loc[:, 'Gender':'Purchase']
    X = data.drop("Product_Category_1", axis=1)
    y = data['Product_Category_1']

    X_train, X_valid, y_train, y_valid = train_test_split(X, y)

    ################# BayesianClassifier ###########################
    bayes_model = GaussianNB()
    bayes_model.fit(X_train, y_train)

    print("GaussianNB train score: ", bayes_model.score(X_train, y_train), file=f)
    print("GaussianNB valid Score: ", bayes_model.score(X_valid, y_valid), file=f)

    # Prediction by using BayesianClassifier
    bayes_predicted = bayes_model.predict(X_valid)
    print("Prediction of GaussianNB model: "
          "products most likely to be purchased from highest occurrence product category#:",
          np.bincount(bayes_predicted).argmax(), file=f)
    print("\n", file=f)

    ################# RandomForestClassifier ########################
    random_forest_model = make_pipeline(
        StandardScaler(),  # Normalize to a predictable range
        RandomForestClassifier(n_estimators=400, max_depth=7)
    )
    random_forest_model.fit(X_train, y_train)

    print("RandomForestClassifier train score: ",
          random_forest_model.score(X_train, y_train), file=f)
    print("RandomForestClassifier valid score: ",
          random_forest_model.score(X_valid, y_valid), file=f)

    # Prediction by using RandomForestClassifier
    rf_predicted = random_forest_model.predict(X_valid)
    print("Prediction of RandomForestClassifier model: "
          "products most likely to be purchased from highest occurrence product category#:",
          np.bincount(rf_predicted).argmax(), file=f)
    print("\n", file=f)

    ################# KNeighborsClassifier #############################
    knn_model = make_pipeline(
        KNeighborsClassifier(n_neighbors=4)
    )
    knn_model.fit(X_train, y_train)

    print("knn_model train score: ",
          knn_model.score(X_train, y_train), file=f)
    print("knn_model valid score: ",
          knn_model.score(X_valid, y_valid), file=f)

    # Prediction by using KNeighborsClassifier
    knn_predicted = knn_model.predict(X_valid)
    print("Prediction of knn_model model: "
          "products most likely to be purchased from highest occurrence product category#:",
          np.bincount(knn_predicted).argmax(), file=f)
    print("\n", file=f)

    ################# DecisionTreeClassifier #############################
    decision_tree_model = DecisionTreeClassifier(min_samples_leaf=4, max_depth=6)
    decision_tree_model.fit(X_train, y_train)

    print("decision_tree_model training score: ",
          decision_tree_model.score(X_train, y_train), file=f)
    print("decision_tree_model valid score: ",
          decision_tree_model.score(X_valid, y_valid), file=f)

    # Prediction by using DecisionTreeClassifier
    decision_tree_predicted = decision_tree_model.predict(X_valid)
    print("Prediction of DecisionTreeClassifier model: "
          "products most likely to be purchased from highest occurrence product category#:",
          np.bincount(decision_tree_predicted).argmax(), file=f)
    print("\n", file=f)

    ################# VotingClassifier #############################
    voting_model = VotingClassifier([
        ('nb', GaussianNB()),
        ('knn', KNeighborsClassifier(4)),
        ('tree1', DecisionTreeClassifier(max_depth=4)),
        ('tree2', DecisionTreeClassifier(min_samples_leaf=10))
    ])
    voting_model.fit(X_train, y_train)

    print("voting_model training score: ",
          voting_model.score(X_train, y_train), file=f)
    print("voting_model valid score: ",
          voting_model.score(X_valid, y_valid), file=f)

    # Prediction by using VotingClassifier
    voting_predicted = voting_model.predict(X_valid)
    print("Prediction of VotingClassifier model: "
          "products most likely to be purchased from highest occurrence product category#:",
          np.bincount(voting_predicted).argmax(), file=f)
    print("\n", file=f)


def main():
    filename = sys.argv[1]

    data = pd.read_csv(filename)

    f = open("Part3_Output/summary.txt", "w")

    MLClassifiers(data, f)

    f.close()


if __name__ == '__main__':
    current_directory = os.getcwd()
    final_directory = os.path.join(
        current_directory, r'Part3_Output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    main()
