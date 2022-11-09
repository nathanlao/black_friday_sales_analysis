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

    # Group By product ID and Age
    grouped_data = dataframe.groupby(by=['Product_ID', 'Age'], as_index=False).count()
    # print(grouped_data)

    # Create a dataFrame for Product_ID and Age
    df = pd.DataFrame(grouped_data, columns=['Product_ID', 'Age'])

    # Age groups and count the number of products in each age groups
    age_groups = df.groupby(by='Age', as_index=False)['Product_ID'].count()
    age_groups = age_groups.rename(columns={'Age': 'Age', 'Product_ID': 'Number of products'})
    # print(age_groups)

    return age_groups['Age'], age_groups['Number of products']


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
