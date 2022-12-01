import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import seaborn
# adapted from https://stackoverflow.com/a/20627316
pd.options.mode.chained_assignment = None


# filter to only show product IDs in a dataframe
def product_filter(data):
    # adapted from https://stackoverflow.com/a/29319200
    return data[['Product_ID']]


# plots the top 5 most popular products
def relation_plotter(data, title):
    plt.title(title)
    # adapted from https://mode.com/python-tutorial/counting-and-plotting-in-python/
    data['Product_ID'].value_counts()[:5].sort_values(
        ascending=True).plot(kind='barh')
    plt.xlabel('Amount sold/purchased')
    plt.ylabel('Product')


# for a particular relation, displays the total amount purchased, graph occurences, and average ranking of products
def product_statistics(relation, f):
    # stores all products
    products = []

    for category in relation:
        # top 5 products in each category with total amount purchased for each respective product
        # adapted from https://stackoverflow.com/a/69301050
        category['Amount'] = category['Product_ID'].map(
            category['Product_ID'].value_counts())
        category = category.drop_duplicates()
        category = category.sort_values(by='Amount', ascending=False)
        category = category[:5]

        # current rank of a product
        rank = 1

        # adapted from https://stackoverflow.com/a/16476974
        for index, row in category.iterrows():
            # boolean to ensure no product is inserted twice
            exists_product = False

            for product in products:
                # if product already exists in products, update the statistics for that product in products
                if row['Product_ID'] == product['product']:
                    product['amount_total'] += row['Amount']
                    product['occurences'] += 1
                    product['rank_total'] = product['rank_total'] + rank
                    product['average_ranking'] = product['rank_total'] / \
                        product['occurences']
                    exists_product = True

            # if product does not exist in products, add it to products
            if exists_product == False:
                new_product = {
                    'product': row['Product_ID'],
                    'amount_total': row['Amount'],
                    'occurences': 1,
                    'rank_total': rank,
                    'average_ranking': rank
                }
                products.append(new_product)

            rank += 1

    # adapted from https://stackoverflow.com/a/12925750
    products = sorted(
        products, key=lambda k: (-k['amount_total'], -k['occurences'], k['average_ranking']))
    for product in products:
        print(product.get('product'), ' was bought ', product.get('amount_total'), ' times among all categories, appears in ', product.get(
            'occurences'), ' different categories, and ranks ', "{:.2f}".format(round(product.get('average_ranking'), 2)), ' on average in a category.', file=f)
    print('\n', file=f)


def age(data, f):
    zero_to_seventeen = data[data['Age'] == '0-17']
    eighteen_to_twenty_five = data[data['Age'] == '18-25']
    twenty_six_to_thirty_five = data[data['Age'] == '26-35']
    thirty_six_to_forty_five = data[data['Age'] == '36-45']
    forty_six_to_fifty = data[data['Age'] == '46-50']
    fifty_one_to_fifty_five = data[data['Age'] == '51-55']
    fifty_five_plus = data[data['Age'] == '55+']

    zero_to_seventeen_products = product_filter(zero_to_seventeen)
    eighteen_to_twenty_five_products = product_filter(eighteen_to_twenty_five)
    twenty_six_to_thirty_five_products = product_filter(
        twenty_six_to_thirty_five)
    thirty_six_to_forty_five_products = product_filter(
        thirty_six_to_forty_five)
    forty_six_to_fifty_products = product_filter(forty_six_to_fifty)
    fifty_one_to_fifty_five_products = product_filter(fifty_one_to_fifty_five)
    fifty_five_plus_products = product_filter(fifty_five_plus)

    plt.figure(figsize=(18, 9))
    plt.subplot(2, 4, 1)
    relation_plotter(zero_to_seventeen_products,
                     'Most popular products among ages 0-17')
    plt.subplot(2, 4, 2)
    relation_plotter(eighteen_to_twenty_five_products,
                     'Most popular products among ages 18-25')
    plt.subplot(2, 4, 3)
    relation_plotter(twenty_six_to_thirty_five_products,
                     'Most popular products among ages 26-35')
    plt.subplot(2, 4, 4)
    relation_plotter(thirty_six_to_forty_five_products,
                     'Most popular products among ages 36-45')
    plt.subplot(2, 4, 5)
    relation_plotter(forty_six_to_fifty_products,
                     'Most popular products among ages 46-50')
    plt.subplot(2, 4, 6)
    relation_plotter(fifty_one_to_fifty_five_products,
                     'Most popular products among ages 51-55')
    plt.subplot(2, 4, 7)
    relation_plotter(fifty_five_plus_products,
                     'Most popular products among ages 55+')
    # adapted from https://stackoverflow.com/a/45239920
    plt.tight_layout()
    plt.savefig(
        'product popularity analysis/age_product_popularity.svg')

    age_categories = [zero_to_seventeen_products, eighteen_to_twenty_five_products, twenty_six_to_thirty_five_products,
                      thirty_six_to_forty_five_products, forty_six_to_fifty_products, fifty_one_to_fifty_five_products, fifty_five_plus_products]
    print('Considering age only (7 categories):', file=f)
    product_statistics(age_categories, f)

    global all_categories
    all_categories += age_categories


def gender(data, f):
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
    plt.savefig(
        'product popularity analysis/gender_product_popularity.svg')

    gender_categories = [male_products, female_products]
    print('Considering gender only (2 categories):', file=f)
    product_statistics(gender_categories, f)

    global all_categories
    all_categories += gender_categories


def marital_status(data, f):
    unmarried = data[data['Marital_Status'] == 0]
    married = data[data['Marital_Status'] == 1]

    unmarried_products = product_filter(unmarried)
    married_products = product_filter(married)

    plt.figure(figsize=(11, 5))
    plt.subplot(1, 2, 1)
    relation_plotter(unmarried_products,
                     'Most popular products among unmarried individuals')
    plt.subplot(1, 2, 2)
    relation_plotter(married_products,
                     'Most popular products among married individuals')
    plt.tight_layout()
    plt.savefig(
        'product popularity analysis/marital_status_product_popularity.svg')

    marital_status_categories = [unmarried_products, married_products]
    print('Considering marital status only (2 categories):', file=f)
    product_statistics(marital_status_categories, f)

    global all_categories
    all_categories += marital_status_categories


def occupation(data, f):
    zero = data[data['Occupation'] == 0]
    one = data[data['Occupation'] == 1]
    two = data[data['Occupation'] == 2]
    three = data[data['Occupation'] == 3]
    four = data[data['Occupation'] == 4]
    five = data[data['Occupation'] == 5]
    six = data[data['Occupation'] == 6]
    seven = data[data['Occupation'] == 7]
    eight = data[data['Occupation'] == 8]
    nine = data[data['Occupation'] == 9]
    ten = data[data['Occupation'] == 10]
    eleven = data[data['Occupation'] == 11]
    twelve = data[data['Occupation'] == 12]
    thirteen = data[data['Occupation'] == 13]
    fourteen = data[data['Occupation'] == 14]
    fifteen = data[data['Occupation'] == 15]
    sixteen = data[data['Occupation'] == 16]
    seventeen = data[data['Occupation'] == 17]
    eighteen = data[data['Occupation'] == 18]
    nineteen = data[data['Occupation'] == 19]
    twenty = data[data['Occupation'] == 20]

    zero_products = product_filter(zero)
    one_products = product_filter(one)
    two_products = product_filter(two)
    three_products = product_filter(three)
    four_products = product_filter(four)
    five_products = product_filter(five)
    six_products = product_filter(six)
    seven_products = product_filter(seven)
    eight_products = product_filter(eight)
    nine_products = product_filter(nine)
    ten_products = product_filter(ten)
    eleven_products = product_filter(eleven)
    twelve_products = product_filter(twelve)
    thirteen_products = product_filter(thirteen)
    fourteen_products = product_filter(fourteen)
    fifteen_products = product_filter(fifteen)
    sixteen_products = product_filter(sixteen)
    seventeen_products = product_filter(seventeen)
    eighteen_products = product_filter(eighteen)
    nineteen_products = product_filter(nineteen)
    twenty_products = product_filter(twenty)

    plt.figure(figsize=(19.75, 9))
    plt.subplot(5, 5, 1)
    relation_plotter(zero_products, 'Most popular products among occupation 0')
    plt.subplot(5, 5, 2)
    relation_plotter(one_products, 'Most popular products among occupation 1')
    plt.subplot(5, 5, 3)
    relation_plotter(two_products, 'Most popular products among occupation 2')
    plt.subplot(5, 5, 4)
    relation_plotter(
        three_products, 'Most popular products among occupation 3')
    plt.subplot(5, 5, 5)
    relation_plotter(four_products, 'Most popular products among occupation 4')
    plt.subplot(5, 5, 6)
    relation_plotter(five_products, 'Most popular products among occupation 5')
    plt.subplot(5, 5, 7)
    relation_plotter(six_products, 'Most popular products among occupation 6')
    plt.subplot(5, 5, 8)
    relation_plotter(
        seven_products, 'Most popular products among occupation 7')
    plt.subplot(5, 5, 9)
    relation_plotter(
        eight_products, 'Most popular products among occupation 8')
    plt.subplot(5, 5, 10)
    relation_plotter(nine_products, 'Most popular products among occupation 9')
    plt.subplot(5, 5, 11)
    relation_plotter(ten_products, 'Most popular products among occupation 10')
    plt.subplot(5, 5, 12)
    relation_plotter(
        eleven_products, 'Most popular products among occupation 11')
    plt.subplot(5, 5, 13)
    relation_plotter(
        twelve_products, 'Most popular products among occupation 12')
    plt.subplot(5, 5, 14)
    relation_plotter(thirteen_products,
                     'Most popular products among occupation 13')
    plt.subplot(5, 5, 15)
    relation_plotter(fourteen_products,
                     'Most popular products among occupation 14')
    plt.subplot(5, 5, 16)
    relation_plotter(fifteen_products,
                     'Most popular products among occupation 15')
    plt.subplot(5, 5, 17)
    relation_plotter(sixteen_products,
                     'Most popular products among occupation 16')
    plt.subplot(5, 5, 18)
    relation_plotter(seventeen_products,
                     'Most popular products among occupation 17')
    plt.subplot(5, 5, 19)
    relation_plotter(eighteen_products,
                     'Most popular products among occupation 18')
    plt.subplot(5, 5, 20)
    relation_plotter(nineteen_products,
                     'Most popular products among occupation 19')
    plt.subplot(5, 5, 21)
    relation_plotter(
        twenty_products, 'Most popular products among occupation 20')
    plt.tight_layout()
    plt.savefig(
        'product popularity analysis/occupation_product_popularity.svg', bbox_inches='tight')

    occupation_categories = [zero_products, one_products, two_products, three_products, four_products, five_products, six_products, seven_products, eight_products, nine_products, ten_products,
                             eleven_products, twelve_products, thirteen_products, fourteen_products, fifteen_products, sixteen_products, seventeen_products, eighteen_products, nineteen_products, twenty_products]
    print('Considering occupation only (21 categories):', file=f)
    product_statistics(occupation_categories, f)

    global all_categories
    all_categories += occupation_categories


def city(data, f):
    a = data[data['City_Category'] == 'A']
    b = data[data['City_Category'] == 'B']
    c = data[data['City_Category'] == 'C']

    a_products = product_filter(a)
    b_products = product_filter(b)
    c_products = product_filter(c)

    plt.figure(figsize=(14, 5))
    plt.subplot(1, 3, 1)
    relation_plotter(a_products, 'Most popular products among city A')
    plt.subplot(1, 3, 2)
    relation_plotter(b_products, 'Most popular products among city B')
    plt.subplot(1, 3, 3)
    relation_plotter(c_products, 'Most popular products among city C')
    plt.tight_layout()
    plt.savefig(
        'product popularity analysis/city_product_popularity.svg')

    city_categories = [a_products, b_products, c_products]
    print('Considering city only (3 categories):', file=f)
    product_statistics(city_categories, f)

    global all_categories
    all_categories += city_categories


def main():
    filename = sys.argv[1]
    data = pd.read_csv(filename)

    # to be used in PART 2
    global all_categories
    all_categories = []

    f = open(
        'product popularity analysis/product_popularity_summary.txt', 'w')

    print('PART 1\nRefer to the graphs to see exactly which products are the most popular in a *specific* category.', file=f)
    print('The summary below combines the information from the graphs to help determine the most popular products in a more *generalized* fashion.', file=f)
    print('Since we only consider the top 5 products for a category in a graph, the average ranking is based on a 5-point scale with a lower number representing a more popular product.', file=f)
    print('Example: Product P ranks 1st in Category A and 3rd in Category B. Average ranking of P = (1 + 3) / 2\n\n', file=f)
    age(data, f)
    gender(data, f)
    marital_status(data, f)
    occupation(data, f)
    city(data, f)

    print('\n\nPART 2\nThe summary belows combines the information from PART 1 to help determine the most popular products generally overall.', file=f)
    print('The number of times a product is bought is calculated by adding the amounts bought for each occurence of that product in PART 1, so it is not reflective of the product\'s overall amount purchased in the data set.', file=f)
    print('Example: Product P was purchased a total of 5 times when considering age and was purchased a total of 10 times when considering gender. Amount of times bought for P = 5 + 10\n\n', file=f)
    product_statistics(all_categories, f)

    f.close()


if __name__ == '__main__':
    seaborn.set()
    # adapted from https://stackoverflow.com/a/14125914
    current_directory = os.getcwd()
    final_directory = os.path.join(
        current_directory, r'product popularity analysis')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    main()
