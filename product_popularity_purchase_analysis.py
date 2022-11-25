import pandas as pd
import matplotlib.pyplot as plt
import sys


# filter to only show product IDs in a dataframe
def product_filter(data):
    return data[['Product_ID']]  # adapted from https://stackoverflow.com/a/29319200


# plots the top 5 most popular products
def relation_plotter(data, title):
    plt.title(title)
    data['Product_ID'].value_counts()[:5].sort_values(ascending=True).plot(
        kind='barh')  # adapted from https://mode.com/python-tutorial/counting-and-plotting-in-python/
    plt.xlabel('Amount purchased')
    plt.ylabel('Product')


def age_relation(data):
    zero_to_seventeen = data[data['Age'] == '0-17']
    eighteen_to_twenty_five = data[data['Age'] == '18-25']
    twenty_six_to_thirty_five = data[data['Age'] == '26-35']
    thirty_six_to_forty_five = data[data['Age'] == '36-45']
    forty_six_to_fifty = data[data['Age'] == '46-50']
    fifty_one_to_fifty_five = data[data['Age'] == '51-55']
    fifty_five_plus = data[data['Age'] == '55+']

    zero_to_seventeen_products = product_filter(zero_to_seventeen)
    eighteen_to_twenty_five_products = product_filter(eighteen_to_twenty_five)
    twenty_six_to_thirty_five_products = product_filter(twenty_six_to_thirty_five)
    thirty_six_to_forty_five_products = product_filter(thirty_six_to_forty_five)
    forty_six_to_fifty_products = product_filter(forty_six_to_fifty)
    fifty_one_to_fifty_five_products = product_filter(fifty_one_to_fifty_five)
    fifty_five_plus_products = product_filter(fifty_five_plus)

    plt.figure(figsize=(18, 9))
    plt.subplot(2, 4, 1)
    relation_plotter(zero_to_seventeen_products, 'Most popular products for ages 0-17')
    plt.subplot(2, 4, 2)
    relation_plotter(eighteen_to_twenty_five_products, 'Most popular products for ages 18-25')
    plt.subplot(2, 4, 3)
    relation_plotter(twenty_six_to_thirty_five_products, 'Most popular products for ages 26-35')
    plt.subplot(2, 4, 4)
    relation_plotter(thirty_six_to_forty_five_products, 'Most popular products for ages 36-45')
    plt.subplot(2, 4, 5)
    relation_plotter(forty_six_to_fifty_products, 'Most popular products for ages 46-50')
    plt.subplot(2, 4, 6)
    relation_plotter(fifty_one_to_fifty_five_products, 'Most popular products for ages 51-55')
    plt.subplot(2, 4, 7)
    relation_plotter(fifty_five_plus_products, 'Most popular products for ages 55+')
    plt.tight_layout()  # adapted from https://stackoverflow.com/a/45239920
    plt.savefig('age_product_popularity.svg')


def gender_relation(data):
    male = data[data['Gender'] == 'M']
    female = data[data['Gender'] == 'F']

    male_products = product_filter(male)
    female_products = product_filter(female)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    relation_plotter(male_products, 'Most popular products among males')
    plt.subplot(1, 2, 2)
    relation_plotter(female_products, 'Most popular products among females')
    plt.tight_layout()
    plt.savefig('gender_product_popularity.svg')


def marital_status_relation(data):
    single = data[data['Marital_Status'] == 0]
    married = data[data['Marital_Status'] == 1]

    single_products = product_filter(single)
    married_products = product_filter(married)

    plt.figure(figsize=(11, 5))
    plt.subplot(1, 2, 1)
    relation_plotter(single_products, 'Most popular products among single individuals')
    plt.subplot(1, 2, 2)
    relation_plotter(married_products, 'Most popular products among married individuals')
    plt.tight_layout()
    plt.savefig('marital_status_product_popularity.svg')


def occupation_relation(data):
    one = data[data['Occupation'] == 0]
    # ... not yet implemented


def city_relation(data):
    a = data[data['City_Category'] == 'A']
    b = data[data['City_Category'] == 'B']
    c = data[data['City_Category'] == 'C']

    a_products = product_filter(a)
    b_products = product_filter(b)
    c_products = product_filter(c)

    plt.figure(figsize=(14, 5))
    plt.subplot(1, 3, 1)
    relation_plotter(a_products, 'Most popular products in city A')
    plt.subplot(1, 3, 2)
    relation_plotter(b_products, 'Most popular products in city B')
    plt.subplot(1, 3, 3)
    relation_plotter(c_products, 'Most popular products in city C')
    plt.tight_layout()
    plt.savefig('city_product_popularity.svg')


def main():
    filename = sys.argv[1]
    data = pd.read_csv(filename)

    age_relation(data)
    gender_relation(data)
    marital_status_relation(data)
    # occupation_relation(data)
    city_relation(data)

    # ... additional analysis based on above information

    # However, it already looks like P00265242 gets purchased the most overall. P00265242 also generally appears 
    # to be the most purchased product among different categories/types of customers


if __name__ == '__main__':
    main()
