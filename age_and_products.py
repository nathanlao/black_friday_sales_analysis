import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def getData():
    filename = sys.argv[1]
    data = pd.read_csv(filename)
    return data


def product_and_age_relation(dataframe):
    # Drop rows if 'Age'/ 'Product_ID' contains NaN values
    dataframe['Age'].dropna(axis=0)
    dataframe['Product_ID'].dropna(axis=0)

    # Group By Age and count the products being purchased in each group of age
    age_group_and_product = dataframe.groupby(by=['Age'])['Product_ID'].agg(
        'size').reset_index(name='product_counts')
    print("There are", age_group_and_product['Age'].count(),
          "groups of age in dataset")

    # Separate 7 age groups
    age_group_one = dataframe[dataframe['Age'] == '0-17']
    age_group_two = dataframe[dataframe['Age'] == '18-25']
    age_group_three = dataframe[dataframe['Age'] == '26-35']
    age_group_four = dataframe[dataframe['Age'] == '36-45']
    age_group_five = dataframe[dataframe['Age'] == '46-50']
    age_group_six = dataframe[dataframe['Age'] == '51-55']
    age_group_seven = dataframe[dataframe['Age'] == '55+']

    # Print total number of products purchased in each ages
    print("Age 0-17 bought", age_group_one['Product_ID'].count(), 'products')
    print("Age 18-25 bought", age_group_two['Product_ID'].count(), 'products')
    print("Age 26-35 bought", age_group_three['Product_ID'].count(),
          'products')
    print("Age 36-45 bought", age_group_four['Product_ID'].count(), 'products')
    print("Age 46-50 bought", age_group_five['Product_ID'].count(), 'products')
    print("Age 51-55 bought", age_group_six['Product_ID'].count(), 'products')
    print("Age 55+ bought", age_group_seven['Product_ID'].count(), 'products')

    # Find the most popular product in each ages
    age_one_id = age_group_one.pivot_table(columns=['Product_ID'],
                                           aggfunc='size')
    age_two_id = age_group_two.pivot_table(columns=['Product_ID'],
                                           aggfunc='size')
    age_three_id = age_group_three.pivot_table(columns=['Product_ID'],
                                               aggfunc='size')
    age_four_id = age_group_four.pivot_table(columns=['Product_ID'],
                                             aggfunc='size')
    age_five_id = age_group_five.pivot_table(columns=['Product_ID'],
                                             aggfunc='size')
    age_six_id = age_group_six.pivot_table(columns=['Product_ID'],
                                           aggfunc='size')
    age_seven_id = age_group_seven.pivot_table(columns=['Product_ID'],
                                               aggfunc='size')
    age_one_max_id = age_one_id.idxmax()
    age_two_max_id = age_two_id.idxmax()
    age_three_max_id = age_three_id.idxmax()
    age_four_max_id = age_four_id.idxmax()
    age_five_max_id = age_five_id.idxmax()
    age_six_max_id = age_six_id.idxmax()
    age_seven_max_id = age_seven_id.idxmax()

    print("The most popular product in age group 0-17:", age_one_max_id)
    print("The most popular product in age group 18-25:", age_two_max_id)
    print("The most popular product in age group 26-35:", age_three_max_id)
    print("The most popular product in age group 36-45:", age_four_max_id)
    print("The most popular product in age group 46-50:", age_five_max_id)
    print("The most popular product in age group 51-55:", age_six_max_id)
    print("The most popular product in age group 55+:", age_seven_max_id)

    return age_group_and_product['Age'], age_group_and_product['product_counts']


def plotAgeAndProducts(age, number_of_products):

    plt.figure(figsize=(15, 4))
    plt.subplot(1, 2, 1)
    plt.title("Relation between age groups and number of products purchased")
    plt.xlabel("Age groups")
    plt.ylabel("Number of product purchased")
    plt.plot(age, number_of_products, color='green', linestyle='dashed',
             linewidth=3, marker='o', markerfacecolor='blue', markersize=12)

    plt.subplot(1, 2, 2)
    plt.title("Relation between age groups and number of products purchased")
    plt.xlabel("Age groups")
    plt.ylabel("Number of product purchased")
    plt.bar(age, number_of_products)
    # plt.show()
    plt.savefig('age_and_products.svg')


def main():

    black_friday_sales_data = getData()
    # print(black_friday_sales_data)

    # Create a dataFrame for data
    dataFrame = pd.DataFrame(black_friday_sales_data)

    # Retrieve age groups and its associated number of products being purchased
    age, number_of_products = product_and_age_relation(dataFrame)

    # TODO: Currently two plots are reflecting the same relations (could combined together later)
    # Bar plot and graph plot showing relationship between age and products
    plotAgeAndProducts(age, number_of_products)


if __name__ == '__main__':
    main()