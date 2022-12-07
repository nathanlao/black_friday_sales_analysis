import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import os
sns.set_theme()
from scipy import stats


def age_and_product_relation(data, f):
    # Drop rows if 'Age'/ 'Product_ID' contains NaN values
    data['Age'].dropna(axis=0)
    data['Product_ID'].dropna(axis=0)

    print("Age and Product Purchase Relation!", file=f)
    print("\n", file=f)

    # Group By Age and count the products being purchased in each group of age
    age_group_and_product = data.groupby(by=['Age'])['Product_ID'].agg(
        'size').reset_index(name='product_counts')
    print("There are", age_group_and_product['Age'].count(),
          "groups of age in dataset", file=f)

    # Separate 7 age groups
    age_group_one = data[data['Age'] == '0-17']
    age_group_two = data[data['Age'] == '18-25']
    age_group_three = data[data['Age'] == '26-35']
    age_group_four = data[data['Age'] == '36-45']
    age_group_five = data[data['Age'] == '46-50']
    age_group_six = data[data['Age'] == '51-55']
    age_group_seven = data[data['Age'] == '55+']

    # Number of products purchased in product category 1 for each age group
    age_one_products = age_group_one.pivot_table(
        columns=['Product_Category_1'],
        aggfunc='size')
    age_two_products = age_group_two.pivot_table(
        columns=['Product_Category_1'],
        aggfunc='size')
    age_three_products = age_group_three.pivot_table(
        columns=['Product_Category_1'],
        aggfunc='size')
    age_four_products = age_group_four.pivot_table(
        columns=['Product_Category_1'],
        aggfunc='size')
    age_five_products = age_group_five.pivot_table(
        columns=['Product_Category_1'],
        aggfunc='size')
    age_six_products = age_group_six.pivot_table(
        columns=['Product_Category_1'],
        aggfunc='size')
    age_seven_products = age_group_seven.pivot_table(
        columns=['Product_Category_1'],
        aggfunc='size')

    # Print total number of products purchased in each ages
    print("Age 0-17 bought", age_group_one['Product_ID'].count(), 'products', file=f)
    print("Age 18-25 bought", age_group_two['Product_ID'].count(), 'products', file=f)
    print("Age 26-35 bought", age_group_three['Product_ID'].count(),
          'products', file=f)
    print("Age 36-45 bought", age_group_four['Product_ID'].count(), 'products', file=f)
    print("Age 46-50 bought", age_group_five['Product_ID'].count(), 'products', file=f)
    print("Age 51-55 bought", age_group_six['Product_ID'].count(), 'products', file=f)
    print("Age 55+ bought", age_group_seven['Product_ID'].count(), 'products', file=f)
    print("\n", file=f)

    # Find the most popular product in each ages (cal duplicates of Product_ID)
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

    age_one_max_id_category = age_group_one[age_group_one['Product_ID'] == age_one_max_id].Product_Category_1.values[0]
    age_two_max_id_category = age_group_two[age_group_two['Product_ID'] == age_two_max_id].Product_Category_1.values[0]
    age_three_max_id_category = age_group_three[age_group_three['Product_ID'] == age_three_max_id].Product_Category_1.values[0]
    age_four_max_id_category = age_group_four[age_group_four['Product_ID'] == age_four_max_id].Product_Category_1.values[0]
    age_five_max_id_category = age_group_five[age_group_five['Product_ID'] == age_five_max_id].Product_Category_1.values[0]
    age_six_max_id_category = age_group_six[age_group_six['Product_ID'] == age_six_max_id].Product_Category_1.values[0]
    age_seven_max_id_category = age_group_seven[age_group_seven['Product_ID'] == age_seven_max_id].Product_Category_1.values[0]

    # Print the most popular productID, its category and total no. of purchases
    print("The most popular product in age group 0-17:", age_one_max_id,
          "and belonged to primary category", age_one_max_id_category,
          ". Total no. of purchases: ", age_one_id[age_one_max_id], file=f)
    print("The most popular product in age group 18-25:", age_two_max_id,
          "and belonged to primary category", age_two_max_id_category,
          ". Total no. of purchases: ", age_two_id[age_two_max_id], file=f)
    print("The most popular product in age group 26-35:", age_three_max_id,
          "and belonged to primary category", age_three_max_id_category,
          ". Total no. of purchases: ", age_three_id[age_three_max_id], file=f)
    print("The most popular product in age group 36-45:", age_four_max_id,
          "and belonged to primary category", age_four_max_id_category,
          ". Total no. of purchases: ", age_four_id[age_four_max_id], file=f)
    print("The most popular product in age group 46-50:", age_five_max_id,
          "and belonged to primary category", age_five_max_id_category,
          ". Total no. of purchases: ", age_five_id[age_five_max_id], file=f)
    print("The most popular product in age group 51-55:", age_six_max_id,
          "and belonged to primary category", age_six_max_id_category,
          ". Total no. of purchases: ", age_six_id[age_six_max_id], file=f)
    print("The most popular product in age group 55+:", age_seven_max_id,
          "and belonged to primary category", age_seven_max_id_category,
          ". Total no. of purchases: ", age_seven_id[age_seven_max_id], file=f)
    print("\n", file=f)

    plt.figure(figsize=(15, 5))
    plt.title("Relation between age groups and total number of products purchased")
    plt.xlabel("Age groups")
    plt.ylabel("Total number of product purchased")
    plt.plot(age_group_and_product['Age'], age_group_and_product['product_counts'], color='green', linestyle='dashed',
             linewidth=3, marker='o', markerfacecolor='blue', markersize=12)
    for x, y in zip(age_group_and_product['Age'], age_group_and_product['product_counts']):
        plt.text(x, y, str(y), color="red", fontsize=12)
    plt.savefig('PartI_Output/age_and_total_products.svg')

    width = 0.1
    plt.figure(figsize=(15, 5))
    plt.title("Age groups product purchases per category")
    plt.xlabel("Ages")
    plt.xticks(range(1, 21))
    plt.ylabel("# of products purchased in each age")
    plt.yscale('log')
    plt.bar(age_one_products.index - 0.4, age_one_products, width, label='0-17')
    plt.bar(age_two_products.index - 0.3, age_two_products, width, label='18-25')
    plt.bar(age_three_products.index - 0.2, age_three_products, width, label='26-35')
    plt.bar(age_four_products.index - 0.1, age_four_products, width, label='36-45')
    plt.bar(age_five_products.index, age_five_products, width, label='46-50')
    plt.bar(age_six_products.index + 0.1, age_six_products, width, label='51-55')
    plt.bar(age_seven_products.index + 0.2, age_seven_products, width, label='55+')
    plt.legend()
    plt.savefig('PartI_Output/age_and_products.svg')


def gender_and_product_relation(data, f):
    print("Gender and Product Purchase Relation:", file=f)
    print("\n", file=f)
    #separate females and males data
    f_purchases = data[(data['Gender'] == 'F')]
    m_purchases = data[(data['Gender'] == 'M')]
    #print the amount of products purchased by females vs males
    print("From our dataset we can see Females bought ", f_purchases['Product_ID'].count(), "and Males bought ", m_purchases['Product_ID'].count(), "products.", file=f)

    #The main reason I decided count how many products in each primary category were bought
    #instead of how many products having the same id was bought
    #is because there is like 3367 product ids and when I plot that
    #you cant even see the product ids, instead If I generalized the products by category then its much easier to
    #plot and much more readable
    #I only chose Product_category_one since there are no null values there as far as I can see, so clearly
    #each product must belong to atleast one category
    #REFERENCE: https://datatofish.com/count-duplicates-pandas/
    f_products = f_purchases.pivot_table(columns=['Product_Category_1'], aggfunc='size')
    m_products = m_purchases.pivot_table(columns=['Product_Category_1'], aggfunc='size')

    #see which product is the most popular for each gender and how much of that product was sold
    #Reference: https://www.geeksforgeeks.org/get-the-index-of-maximum-value-in-dataframe-column/
    #Reference: https://stackoverflow.com/questions/61964973/pandas-get-column-value-where-row-matches-condition
    f_product_id =  f_purchases.pivot_table(columns=['Product_ID'], aggfunc='size')
    m_product_id = m_purchases.pivot_table(columns=['Product_ID'], aggfunc='size')
    f_maxid =f_product_id.idxmax()
    m_maxid =m_product_id.idxmax()
    print("The most popular product for females had Product_ID: ", f_maxid, "and belonged to primary category", f_purchases[(f_purchases['Product_ID'] == f_maxid)].Product_Category_1.values[0], ".", f_product_id[f_maxid], "purchases of this product was made by females.", file=f)

    print("The most popular product for males had Product_ID: ", m_maxid, "and belonged to primary category", m_purchases[(m_purchases['Product_ID'] == m_maxid)].Product_Category_1.values[0], ".", m_product_id[m_maxid], "purchases of this product was made by males.", file=f)

    #plot the amount of products purchased per category for each gender
    plt.figure(figsize=(15,6))

    #plot the female purchases
    plt.title("Female vs Male product purchases per category")
    plt.xlabel("Product_Category#")
    plt.xticks(range(1,21))
    plt.ylabel("# of products purchased in each category")
    plt.yscale('log') #chose log scale since if I plot directly it seems like category 9 and 17 have 0 purtchases since its so low
    #Reference: https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
    plt.bar(f_products.index-0.2, f_products, 0.4, label = 'Female')

    #plot the male purchases
    plt.bar(m_products.index+0.2, m_products, 0.4, label = 'Male')
    plt.legend()
    #plt.show()
    plt.savefig('PartI_Output/gender_and_products.svg')

    #for chi-squared test
    #creates a table with gender as rows and product category as cols and the number of products bought per category as the values
    #print contingency table if confused
    dataset = data[['Product_ID', 'Gender', 'Product_Category_1']]
    grouped_data = dataset.groupby(['Gender', 'Product_Category_1']).count()
    grouped_data.rename(columns = {'Product_ID': '#Products_bought'}, inplace = True)
    grouped_data = grouped_data.reset_index()
    contingency = grouped_data.pivot(index="Gender", columns="Product_Category_1", values="#Products_bought")
    (contingency.T).to_csv('PartI_Output/Gender_purchases.csv')# create a file with this table to view later
    #print p value where is p< 0.05 then the genders affects the categories of products bought
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print("Chi-Squared p-value: ", p, file=f)
    print("\n", file=f)


def martial_and_product_relation(data, f):
    print("Marital Status and Product Purchase Relation:", file=f)
    print("\n", file=f)
    #separate married/unmarried data
    married = data[(data['Marital_Status'] == 1)]
    unmarried = data[(data['Marital_Status'] == 0)]

    #print the amount of products purchased by married vs not-married people
    print("From our dataset we can see married people bought ", married['Product_ID'].count(), "and unmarried people bought ", unmarried['Product_ID'].count(), "products.", file=f)

    #counts how many products in each category (per married and unmarried)
    #creates a two col table left is category# right is how many products
    married_products = married.pivot_table(columns=['Product_Category_1'], aggfunc='size')
    unmarried_products = unmarried.pivot_table(columns=['Product_Category_1'], aggfunc='size')

    #see which product is the most popular for each marital status and how much of that product was sold
    m_product_id =  married.pivot_table(columns=['Product_ID'], aggfunc='size')
    um_product_id = unmarried.pivot_table(columns=['Product_ID'], aggfunc='size')
    m_maxid = m_product_id.idxmax()
    um_maxid = um_product_id.idxmax()
    print("The most popular product for married people had Product_ID: ", m_maxid, "and belonged to primary category", married[(married['Product_ID'] == m_maxid)].Product_Category_1.values[0], ".", m_product_id[m_maxid], "purchases of this product was made by married people.", file=f)

    print("The most popular product for unmarried people had Product_ID: ", um_maxid, "and belonged to primary category", unmarried[(unmarried['Product_ID'] == um_maxid)].Product_Category_1.values[0], ".", um_product_id[um_maxid], "purchases of this product was made by unmarried people.", file=f)

    #plot the amount of products purchased per category for each gender
    plt.figure(figsize=(15,6))

    #plot the married people purchases
    plt.title("Married vs Unmarried people product purchases per category")
    plt.xlabel("Product_Category#")
    plt.xticks(range(1,21))
    plt.ylabel("# of products purchased in each category")
    plt.yscale('log') #chose log scale since if I plot directly it seems like category 9 and 17 have 0 purtchases since its so low
    #Reference: https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
    plt.bar(married_products.index-0.2, married_products, 0.4, label = 'Married')

    #plot the unmarried people purchases
    plt.bar(unmarried_products.index+0.2, unmarried_products,0.4, label = 'Unmarried')
    plt.legend()
    #plt.show()
    plt.savefig('PartI_Output/Martial_status_and_products.svg')

    #for chi-squared test
    #creates a table with marital status as rows and product category as cols and the number of products bought per category as the values
    #print contingency table if confused
    dataset = data[['Product_ID', 'Marital_Status', 'Product_Category_1']]
    grouped_data = dataset.groupby(['Marital_Status', 'Product_Category_1']).count()
    grouped_data.rename(columns = {'Product_ID': '#Products_bought'}, inplace = True)
    grouped_data = grouped_data.reset_index()
    contingency = grouped_data.pivot(index="Marital_Status", columns="Product_Category_1", values="#Products_bought")
    (contingency.T).to_csv('PartI_Output/Marital_status_purchases.csv')# create a file with this table to view later
    #print p value where is p< 0.05 then the marital status affects the categories of products bought
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print("Chi-Squared p-value: ", p, file=f)
    print("\n", file=f)


def occupation_and_product_relation(data, f):
    print("Occupation and Product Purchase Relation:", file=f)
    print("\n", file=f)
    #groupby occupation and product category 1
    dataset = data[['Product_ID', 'Occupation', 'Product_Category_1']]
    grouped_data = dataset.groupby(['Occupation', 'Product_Category_1']).count()
    grouped_data.rename(columns = {'Product_ID': '#Products_bought'}, inplace = True)
    grouped_data = grouped_data.reset_index()

    purchasedata = grouped_data.pivot(index="Occupation", columns="Product_Category_1", values="#Products_bought") #get into the table format for heatmap
    purchasedata = purchasedata.fillna(0)#incase any occupation didn't but from a category there will be NaN there so change it to zero (eg, for occ 8 and cat 14)
    purchasedata = purchasedata.astype('int') #change data type from float to int since it's all whole numbers
    purchasedataTransposed = purchasedata.T #in this cols are occupation and rows are product category
    purchasedataTransposed.to_csv('PartI_Output/Occupation_purchases.csv')# create a file with this table to view later

    occ = 0
    maxprodnum = 0
    occmax = 0
    for occ in range(len(purchasedataTransposed.columns)):
        maxValuesindx = purchasedataTransposed[occ].idxmax()
        print("Max Number of products bought by people in Occupation", occ, "is", purchasedataTransposed[occ][maxValuesindx], "which belongs to product category", maxValuesindx, file=f)
        if purchasedataTransposed[occ][maxValuesindx] > maxprodnum:
            maxprodnum = purchasedataTransposed[occ][maxValuesindx]
            occmax = occ

    print("The maximum number of products was bought by people in Occupation", occmax, file=f)

    #chi-squared test to determine if the occupation had any effect on the categories of products bought
    #if p < 0.05 then it does affect it
    chi2, p, dof, expected = stats.chi2_contingency(purchasedata)
    print("Chi-Squared p-value: ", p, file=f)
    print("\n", file=f)

    #plot them on a heat map by occupation and product category
    #References: https://www.statology.org/save-seaborn-plot/
    #https://machinelearningknowledge.ai/seaborn-heatmap-using-sns-heatmap-with-examples-for-beginners/
    #https://stackoverflow.com/questions/33104322/auto-adjust-font-size-in-seaborn-heatmap
    #https://seaborn.pydata.org/examples/spreadsheet_heatmap.html
    f, ax = plt.subplots(figsize=(25,25))
    heatmap = sns.heatmap(purchasedata, annot=True, linewidths = 1, ax=ax, cmap="OrRd")
    plt.title('Products bought in each Category per Occupation', fontsize = 20) # title with fontsize 20
    plt.xlabel('Product_Category', fontsize = 15) # x-axis label with fontsize 15
    plt.ylabel('Occupation', fontsize = 15) # y-axis label with fontsize 15
    fig = heatmap.get_figure()
    fig.savefig('PartI_Output/OccupationPurchasesHeatmap.svg')


def city_and_product_relation(data, f):
    print("City and Product Purchase Relation:", file=f)
    print("\n", file=f)
    dataset = data[['Product_ID', 'City_Category', 'Product_Category_1']]
    grouped_data = dataset.groupby(['City_Category', 'Product_Category_1']).count()
    grouped_data.rename(columns = {'Product_ID': '#Products_bought'}, inplace = True)
    grouped_data = grouped_data.reset_index()
    city_data = grouped_data.pivot(index="City_Category", columns="Product_Category_1", values="#Products_bought")
    city_data_T = city_data.T #transpose so that product category is index and city category is col headers
    city_data_T.to_csv('PartI_Output/city_purchases.csv')# create a file with this table to view later

    #print some results to the txt
    #print the amount of products purchased by each city category people
    print("From our dataset we can see City A people bought ", city_data_T['A'].sum(), "and city B people bought ", city_data_T['B'].sum(), "and city C people bought ", city_data_T['C'].sum(),"products.", file=f)
    #print the most popoular product categories per city
    max_A = city_data_T['A'].idxmax()
    max_B = city_data_T['B'].idxmax()
    max_C = city_data_T['C'].idxmax()
    print("most popular product category for city A is", max_A, "with", city_data_T['A'][max_A], "product purchases.", file = f)
    print("most popular product category for city B is", max_B, "with", city_data_T['B'][max_B], "product purchases.", file = f)
    print("most popular product category for city C is", max_C, "with", city_data_T['C'][max_C], "product purchases.", file = f)

    #plot the city vs purchases
    plt.figure(figsize=(15,6))
    plt.title("People in City's A,B,C and their product purchases per category")
    plt.xlabel("Product_Category#")
    plt.xticks(range(1,21))
    plt.ylabel("# of products purchased in each category")
    plt.yscale('log')
    #Reference: https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
    #plot city A purchases
    plt.bar(city_data_T.index-0.2, city_data_T['A'], 0.2, label = 'City A')

    #plot the city B purchases
    plt.bar(city_data_T.index, city_data_T['B'],0.2, label = 'City B')
    #plot the city C purchases
    plt.bar(city_data_T.index+0.2, city_data_T['C'], 0.2, label = 'City C')
    plt.legend()
    #plt.show()
    plt.savefig('PartI_Output/City_and_products.svg')
    #print p value where is p< 0.05 then the marital status affects the categories of products bought
    chi2, p, dof, expected = stats.chi2_contingency(city_data)
    print("Chi-Squared p-value: ", p, file=f)
    print("\n", file=f)


def main():
    filename = sys.argv[1]
    data = pd.read_csv(filename)
    #Reference: https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    f = open("PartI_Output/summary.txt", "w")

    age_and_product_relation(data, f)

    gender_and_product_relation(data, f)

    martial_and_product_relation(data, f)

    occupation_and_product_relation(data, f)

    city_and_product_relation(data, f)
    f.close()

if __name__ == '__main__':
    #Reference: https://stackoverflow.com/a/14125914
    current_directory = os.getcwd()
    final_directory = os.path.join(
        current_directory, r'PartI_Output')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    main()