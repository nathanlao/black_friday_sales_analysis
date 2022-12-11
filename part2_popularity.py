import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
pd.options.mode.chained_assignment = None  # adapted from https://stackoverflow.com/a/20627316


# filter data to only consider 'Product_ID' column and retrieve top 5 products with total amount purchased for each respective product
# input: dataframe
def product_filter(data):
    data =  data[['Product_ID']]
    data['Amount_Purchased'] = data['Product_ID'].map(data['Product_ID'].value_counts())  # adapted from https://stackoverflow.com/a/69301050
    data = data.drop_duplicates()
    data = data.sort_values(by='Amount_Purchased', ascending=False)
    data = data[:5]
    return data


# makes graph for top 5 most popular products in a category
# input: dataframe, title of graph
def category_plotter(data, title):
    plt.title(title)
    plot = sns.barplot(data=data, x='Amount_Purchased', y='Product_ID')
    plt.bar_label(plot.containers[0], size=12, label_type='center', color='w')  # adapted from https://datavizpyr.com/annotate-barplot-with-bar_label-in-matplotlib/
    plt.xlabel('Amount sold/purchased')
    plt.ylabel('Product')


# for each unique product in a particular relation: prints out total amount purchased, category/graph occurences, and average ranking 
# input: relation (ex. age relation which contains age categories 0-17, 18-25, etc.), text file to write to
def product_statistics(relation, f):
    # stores all unique products in relation (ex. a product could appear in multiple graphs, but we only want to count it once)
    unique_products = []

    for category in relation:
        # iteration through category always starts with most popular product (or 1st rank) for that category (because each category is sorted from above)
        rank = 1

        # iterate through products in category
        for index, row in category.iterrows():  # adapted from https://stackoverflow.com/a/16476974
            # boolean ensures that no product is inserted twice into 'unique_products' array
            exists_product = False

            for product in unique_products:
                # if product already exists in 'unique_products' array, update statistics for that product in 'unique_products' array
                if row['Product_ID'] == product['product']:
                    product['amount_total'] += row['Amount_Purchased']
                    product['occurences'] += 1
                    product['rank_total'] = product['rank_total'] + rank
                    product['average_ranking'] = product['rank_total'] / product['occurences']
                    exists_product = True

            # if product does not already exist in 'unique_products' array, add it to 'unique_products' array
            if exists_product == False:
                new_product = {
                    'product': row['Product_ID'],
                    'amount_total': row['Amount_Purchased'],
                    'occurences': 1,
                    'rank_total': rank,
                    'average_ranking': rank
                }
                unique_products.append(new_product)

            rank += 1

    # sort 'unique_products' array for printing
    unique_products = sorted(unique_products, key=lambda k: (-k['amount_total'], -k['occurences'], k['average_ranking']))  # adapted from https://stackoverflow.com/a/12925750

    # print statistics for each product
    for product in unique_products:
        print(product.get('product'), ' was bought ', product.get('amount_total'), ' times among all categories, appears in ', product.get('occurences'), ' different categories, and ranks ', "{:.2f}".format(round(product.get('average_ranking'), 2)), ' on average in a category.', file=f)
    
    print('', file=f)


# input: dataframe, text file to write to
def age_relation(data, f):
    # split relation into respective categories and filter according to 'product_filter' function
    zero_to_seventeen = product_filter(data[data['Age'] == '0-17'])
    eighteen_to_twenty_five = product_filter(data[data['Age'] == '18-25'])
    twenty_six_to_thirty_five = product_filter(data[data['Age'] == '26-35'])
    thirty_six_to_forty_five = product_filter(data[data['Age'] == '36-45'])
    forty_six_to_fifty = product_filter(data[data['Age'] == '46-50'])
    fifty_one_to_fifty_five = product_filter(data[data['Age'] == '51-55'])
    fifty_five_plus = product_filter(data[data['Age'] == '55+'])

    # create graph for each category and save graphs as svg
    plt.figure(figsize=(19, 9))
    plt.subplot(2, 4, 1)
    category_plotter(zero_to_seventeen, 'Most popular products among ages 0-17')
    plt.subplot(2, 4, 2)
    category_plotter(eighteen_to_twenty_five, 'Most popular products among ages 18-25')
    plt.subplot(2, 4, 3)
    category_plotter(twenty_six_to_thirty_five, 'Most popular products among ages 26-35')
    plt.subplot(2, 4, 4)
    category_plotter(thirty_six_to_forty_five, 'Most popular products among ages 36-45')
    plt.subplot(2, 4, 5)
    category_plotter(forty_six_to_fifty, 'Most popular products among ages 46-50')
    plt.subplot(2, 4, 6)
    category_plotter(fifty_one_to_fifty_five, 'Most popular products among ages 51-55')
    plt.subplot(2, 4, 7)
    category_plotter(fifty_five_plus, 'Most popular products among ages 55+')
    plt.tight_layout()  # adapted from https://stackoverflow.com/a/45239920
    plt.savefig('Part2_Output/only_age_popularity.svg')

    # use 'product_statistics' function to get additional information about age relation
    age_categories = [zero_to_seventeen, eighteen_to_twenty_five, twenty_six_to_thirty_five, thirty_six_to_forty_five, forty_six_to_fifty, fifty_one_to_fifty_five, fifty_five_plus]
    print('Considering age relation only (7 total categories, refer to \'only_age_popularity.svg\'):', file=f)
    product_statistics(age_categories, f)

    # add all age categories to global function which will be used in PART 2 of text file (which is explained in main function)
    global all_categories
    all_categories += age_categories


# input: dataframe, text file to write to
def gender_relation(data, f):
    male = product_filter(data[data['Gender'] == 'M'])
    female = product_filter(data[data['Gender'] == 'F'])

    plt.figure(figsize=(11, 5))
    plt.subplot(1, 2, 1)
    category_plotter(male, 'Most popular products among males')
    plt.subplot(1, 2, 2)
    category_plotter(female, 'Most popular products among females')
    plt.tight_layout()
    plt.savefig('Part2_Output/only_gender_popularity.svg')

    gender_categories = [male, female]
    print('Considering gender relation only (2 total categories, refer to \'only_gender_popularity.svg\'):', file=f)
    product_statistics(gender_categories, f)

    global all_categories
    all_categories += gender_categories


# input: dataframe, text file to write to
def marital_status_relation(data, f):
    unmarried = product_filter(data[data['Marital_Status'] == 0])
    married = product_filter(data[data['Marital_Status'] == 1])

    plt.figure(figsize=(11, 5))
    plt.subplot(1, 2, 1)
    category_plotter(unmarried, 'Most popular products among unmarried individuals')
    plt.subplot(1, 2, 2)
    category_plotter(married, 'Most popular products among married individuals')
    plt.tight_layout()
    plt.savefig('Part2_Output/only_marital_status_popularity.svg')

    marital_status_categories = [unmarried, married]
    print('Considering marital status relation only (2 total categories, refer to \'only_marital_status_popularity.svg\'):', file=f)
    product_statistics(marital_status_categories, f)

    global all_categories
    all_categories += marital_status_categories


# input: dataframe, text file to write to
def occupation_relation(data, f):
    zero = product_filter(data[data['Occupation'] == 0])
    one = product_filter(data[data['Occupation'] == 1])
    two = product_filter(data[data['Occupation'] == 2])
    three = product_filter(data[data['Occupation'] == 3])
    four = product_filter(data[data['Occupation'] == 4])
    five = product_filter(data[data['Occupation'] == 5])
    six = product_filter(data[data['Occupation'] == 6])
    seven = product_filter(data[data['Occupation'] == 7])
    eight = product_filter(data[data['Occupation'] == 8])
    nine = product_filter(data[data['Occupation'] == 9])
    ten = product_filter(data[data['Occupation'] == 10])
    eleven = product_filter(data[data['Occupation'] == 11])
    twelve = product_filter(data[data['Occupation'] == 12])
    thirteen = product_filter(data[data['Occupation'] == 13])
    fourteen = product_filter(data[data['Occupation'] == 14])
    fifteen = product_filter(data[data['Occupation'] == 15])
    sixteen = product_filter(data[data['Occupation'] == 16])
    seventeen = product_filter(data[data['Occupation'] == 17])
    eighteen = product_filter(data[data['Occupation'] == 18])
    nineteen = product_filter(data[data['Occupation'] == 19])
    twenty = product_filter(data[data['Occupation'] == 20])

    plt.figure(figsize=(19.75, 9.5))
    plt.subplot(5, 5, 1)
    category_plotter(zero, 'Most popular products among occupation 0')
    plt.subplot(5, 5, 2)
    category_plotter(one, 'Most popular products among occupation 1')
    plt.subplot(5, 5, 3)
    category_plotter(two, 'Most popular products among occupation 2')
    plt.subplot(5, 5, 4)
    category_plotter(three, 'Most popular products among occupation 3')
    plt.subplot(5, 5, 5)
    category_plotter(four, 'Most popular products among occupation 4')
    plt.subplot(5, 5, 6)
    category_plotter(five, 'Most popular products among occupation 5')
    plt.subplot(5, 5, 7)
    category_plotter(six, 'Most popular products among occupation 6')
    plt.subplot(5, 5, 8)
    category_plotter(seven, 'Most popular products among occupation 7')
    plt.subplot(5, 5, 9)
    category_plotter(eight, 'Most popular products among occupation 8')
    plt.subplot(5, 5, 10)
    category_plotter(nine, 'Most popular products among occupation 9')
    plt.subplot(5, 5, 11)
    category_plotter(ten, 'Most popular products among occupation 10')
    plt.subplot(5, 5, 12)
    category_plotter(eleven, 'Most popular products among occupation 11')
    plt.subplot(5, 5, 13)
    category_plotter(twelve, 'Most popular products among occupation 12')
    plt.subplot(5, 5, 14)
    category_plotter(thirteen, 'Most popular products among occupation 13')
    plt.subplot(5, 5, 15)
    category_plotter(fourteen, 'Most popular products among occupation 14')
    plt.subplot(5, 5, 16)
    category_plotter(fifteen, 'Most popular products among occupation 15')
    plt.subplot(5, 5, 17)
    category_plotter(sixteen, 'Most popular products among occupation 16')
    plt.subplot(5, 5, 18)
    category_plotter(seventeen, 'Most popular products among occupation 17')
    plt.subplot(5, 5, 19)
    category_plotter(eighteen, 'Most popular products among occupation 18')
    plt.subplot(5, 5, 20)
    category_plotter(nineteen, 'Most popular products among occupation 19')
    plt.subplot(5, 5, 21)
    category_plotter(twenty, 'Most popular products among occupation 20')
    plt.tight_layout()
    plt.savefig('Part2_Output/only_occupation_popularity.svg', bbox_inches='tight')

    occupation_categories = [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty]
    print('Considering occupation relation only (21 total categories, refer to \'only_occupation_popularity.svg\'):', file=f)
    product_statistics(occupation_categories, f)

    global all_categories
    all_categories += occupation_categories


# input: dataframe, text file to write to
def city_relation(data, f):
    a = product_filter(data[data['City_Category'] == 'A'])
    b = product_filter(data[data['City_Category'] == 'B'])
    c = product_filter(data[data['City_Category'] == 'C'])

    plt.figure(figsize=(14, 5))
    plt.subplot(1, 3, 1)
    category_plotter(a, 'Most popular products among city A')
    plt.subplot(1, 3, 2)
    category_plotter(b, 'Most popular products among city B')
    plt.subplot(1, 3, 3)
    category_plotter(c, 'Most popular products among city C')
    plt.tight_layout()
    plt.savefig('Part2_Output/only_city_popularity.svg')

    city_categories = [a, b, c]
    print('Considering city relation only (3 total categories, refer to \'only_city_popularity.svg\'):', file=f)
    product_statistics(city_categories, f)

    global all_categories
    all_categories += city_categories


# input: dataframe, text file to write to
def gender_age_relation(data, f):
    male = data[data['Gender'] == 'M']
    female = data[data['Gender'] == 'F']

    male_zero_to_seventeen = product_filter(male[male['Age'] == '0-17'])
    male_eighteen_to_twenty_five = product_filter(male[male['Age'] == '18-25'])
    male_twenty_six_to_thirty_five = product_filter(male[male['Age'] == '26-35'])
    male_thirty_six_to_forty_five = product_filter(male[male['Age'] == '36-45'])
    male_forty_six_to_fifty = product_filter(male[male['Age'] == '46-50'])
    male_fifty_one_to_fifty_five = product_filter(male[male['Age'] == '51-55'])
    male_fifty_five_plus = product_filter(male[male['Age'] == '55+'])

    plt.figure(figsize=(19, 9))
    plt.subplot(2, 4, 1)
    category_plotter(male_zero_to_seventeen, 'Most popular products among males aged 0-17')
    plt.subplot(2, 4, 2)
    category_plotter(male_eighteen_to_twenty_five, 'Most popular products among males aged 18-25')
    plt.subplot(2, 4, 3)
    category_plotter(male_twenty_six_to_thirty_five, 'Most popular products among males aged 26-35')
    plt.subplot(2, 4, 4)
    category_plotter(male_thirty_six_to_forty_five, 'Most popular products among males aged 36-45')
    plt.subplot(2, 4, 5)
    category_plotter(male_forty_six_to_fifty, 'Most popular products among males aged 46-50')
    plt.subplot(2, 4, 6)
    category_plotter(male_fifty_one_to_fifty_five, 'Most popular products among males aged 51-55')
    plt.subplot(2, 4, 7)
    category_plotter(male_fifty_five_plus, 'Most popular products among males aged 55+')
    plt.tight_layout()
    plt.savefig('Part2_Output/combined_male_age_popularity.svg')

    male_age_categories = [male_zero_to_seventeen, male_eighteen_to_twenty_five, male_twenty_six_to_thirty_five, male_thirty_six_to_forty_five, male_forty_six_to_fifty, male_fifty_one_to_fifty_five, male_fifty_five_plus]
    print('Considering males and their age (7 total categories, refer to \'combined_male_age_popularity.svg\'):', file=f)
    product_statistics(male_age_categories, f)

    female_zero_to_seventeen = product_filter(female[female['Age'] == '0-17'])
    female_eighteen_to_twenty_five = product_filter(female[female['Age'] == '18-25'])
    female_twenty_six_to_thirty_five = product_filter(female[female['Age'] == '26-35'])
    female_thirty_six_to_forty_five = product_filter(female[female['Age'] == '36-45'])
    female_forty_six_to_fifty = product_filter(female[female['Age'] == '46-50'])
    female_fifty_one_to_fifty_five = product_filter(female[female['Age'] == '51-55'])
    female_fifty_five_plus = product_filter(female[female['Age'] == '55+'])

    plt.figure(figsize=(19, 9))
    plt.subplot(2, 4, 1)
    category_plotter(female_zero_to_seventeen, 'Most popular products among females aged 0-17')
    plt.subplot(2, 4, 2)
    category_plotter(female_eighteen_to_twenty_five, 'Most popular products among females aged 18-25')
    plt.subplot(2, 4, 3)
    category_plotter(female_twenty_six_to_thirty_five, 'Most popular products among females aged 26-35')
    plt.subplot(2, 4, 4)
    category_plotter(female_thirty_six_to_forty_five, 'Most popular products among females aged 36-45')
    plt.subplot(2, 4, 5)
    category_plotter(female_forty_six_to_fifty, 'Most popular products among females aged 46-50')
    plt.subplot(2, 4, 6)
    category_plotter(female_fifty_one_to_fifty_five, 'Most popular products among females aged 51-55')
    plt.subplot(2, 4, 7)
    category_plotter(female_fifty_five_plus, 'Most popular products among females aged 55+')
    plt.tight_layout()
    plt.savefig('Part2_Output/combined_female_age_popularity.svg')

    female_age_categories = [female_zero_to_seventeen, female_eighteen_to_twenty_five, female_twenty_six_to_thirty_five, female_thirty_six_to_forty_five, female_forty_six_to_fifty, female_fifty_one_to_fifty_five, female_fifty_five_plus]
    print('Considering females and their age (7 total categories, refer to \'combined_female_age_popularity.svg\'):', file=f)
    product_statistics(female_age_categories, f)


# input: dataframe, text file to write to
def gender_marital_status_relation(data, f):
    male = data[data['Gender'] == 'M']
    female = data[data['Gender'] == 'F']

    male_unmarried = product_filter(male[male['Marital_Status'] == 0])
    male_married = product_filter(male[male['Marital_Status'] == 1])

    plt.figure(figsize=(11, 5))
    plt.subplot(1, 2, 1)
    category_plotter(male_unmarried, 'Most popular products among unmarried males')
    plt.subplot(1, 2, 2)
    category_plotter(male_married, 'Most popular products among married males')
    plt.tight_layout()
    plt.savefig('Part2_Output/combined_male_marital_status_popularity.svg')

    male_marital_status_categories = [male_unmarried, male_married]
    print('Considering males and their marital status (2 total categories, refer to \'combined_male_marital_status_popularity.svg\'):', file=f)
    product_statistics(male_marital_status_categories, f)

    female_unmarried = product_filter(female[female['Marital_Status'] == 0])
    female_married = product_filter(female[female['Marital_Status'] == 1])

    plt.figure(figsize=(11, 5))
    plt.subplot(1, 2, 1)
    category_plotter(female_unmarried, 'Most popular products among unmarried females')
    plt.subplot(1, 2, 2)
    category_plotter(female_married, 'Most popular products among married females')
    plt.tight_layout()
    plt.savefig('Part2_Output/combined_female_marital_status_popularity.svg')

    female_marital_status_categories = [female_unmarried, female_married]
    print('Considering females and their marital status (2 total categories, refer to \'combined_female_marital_status_popularity.svg\'):', file=f)
    product_statistics(female_marital_status_categories, f)


def main():
    filename = sys.argv[1]
    data = pd.read_csv(filename)

    # used in PART 2 of text file (which is explained in print statements below)
    global all_categories
    all_categories = []

    f = open('Part2_Output/popularity_summaries.txt', 'w')

    print('Refer to the popularity graphs to see exactly which products are the most popular in a *specific* category. The summaries below combine the information from the graphs to help determine the most popular products in a more *generalized* fashion.', file=f)
    print('Example: Relation R contains 5 different categories/graphs. If all 5 categories/graphs were combined into one, there would be a certain number of *unique* products displayed. A summary does this combination and calculates a few statistics for *each* unique product (specifically among the 5 categories).', file=f)
    print('\nSince we only consider the top 5 products for a category, the average ranking is calculated out of 5 with a lower number representing a more popular product.', file=f)
    print('Example: Product P ranks 1st in Category A and 3rd in Category B for a particular relation. Average ranking of P = (1 + 3) / 2', file=f)

    print('\n\n\nPART 1\n', file=f)
    age_relation(data, f)
    gender_relation(data, f)
    marital_status_relation(data, f)
    occupation_relation(data, f)
    city_relation(data, f)

    print('\n\nPART 2\nThe summary below combines the information from PART 1 to help determine the most popular products generally overall.', file=f)
    print('\nThe number of times a product is bought in PART 2 is calculated by adding together *each* occurence of the number of times that product is bought in PART 1. Therefore, the \'times bought\' statistic is not reflective of a product\'s overall occurence in the data set.', file=f)
    print('Example: Product P was purchased a total of 5 times when considering age and was purchased a total of 10 times when considering gender. Amount of times bought for P = 5 + 10\n', file=f)
    product_statistics(all_categories, f)

    print('\n\nPART 3\nThe summaries below are the results of combining *multiple* relations.\n', file=f)
    gender_age_relation(data, f)
    gender_marital_status_relation(data, f)

    f.close()


if __name__ == '__main__':
    sns.set_theme(style='ticks', palette='blend:#6C2B6D,#E98D6B')

    # all files created by this program will be outputted to 'Part2_Output' folder
    current_directory = os.getcwd()  # adapted from https://stackoverflow.com/a/14125914
    final_directory = os.path.join(current_directory, r'Part2_Output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    main()
