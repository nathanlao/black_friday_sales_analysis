import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def gender_and_product_relation(data, f):
    print("Gender and Product Purchase Relation!", file=f)
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
    plt.figure(figsize=(15,4))

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
    plt.savefig('gender_and_products.svg')
    print("\n", file=f)
 

def martial_and_product_relation(data, f):
    print("Martial Status and Product Purchase Relation!", file=f)
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
    plt.figure(figsize=(15,4))

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
    plt.savefig('Martial_status_and_products.svg')
    print("\n", file=f)
 
def occupation_and_product_relation(data, f):
    print("Occupation and Product Purchase Relation!", file=f)
    print("\n", file=f)
    #groupby occupation and product category 1
    dataset = data[['Product_ID', 'Occupation', 'Product_Category_1']]
    grouped_data = dataset.groupby(['Occupation', 'Product_Category_1']).count()
    grouped_data.rename(columns = {'Product_ID': '#Products_bought'}, inplace = True)
    grouped_data = grouped_data.reset_index()
    
    #split into dataframes by Occupation number
    Occ0 = grouped_data[(grouped_data['Occupation'] == 0)]
    Occ1 = grouped_data[(grouped_data['Occupation'] == 1)].reset_index()
    Occ2 = grouped_data[(grouped_data['Occupation'] == 2)].reset_index()
    Occ3 = grouped_data[(grouped_data['Occupation'] == 3)].reset_index()
    Occ4 = grouped_data[(grouped_data['Occupation'] == 4)].reset_index()
    Occ5 = grouped_data[(grouped_data['Occupation'] == 5)].reset_index()
    Occ6 = grouped_data[(grouped_data['Occupation'] == 6)].reset_index()
    Occ7 = grouped_data[(grouped_data['Occupation'] == 7)].reset_index()
    Occ8 = grouped_data[(grouped_data['Occupation'] == 8)].reset_index()#never buys from product category 14
    Occ9 = grouped_data[(grouped_data['Occupation'] == 9)].reset_index()
    Occ10 = grouped_data[(grouped_data['Occupation'] == 10)].reset_index()
    Occ11 = grouped_data[(grouped_data['Occupation'] == 11)].reset_index()
    Occ12 = grouped_data[(grouped_data['Occupation'] == 12)].reset_index()
    Occ13 = grouped_data[(grouped_data['Occupation'] == 13)].reset_index()
    Occ14 = grouped_data[(grouped_data['Occupation'] == 14)].reset_index()
    Occ15 = grouped_data[(grouped_data['Occupation'] == 15)].reset_index()
    Occ16 = grouped_data[(grouped_data['Occupation'] == 16)].reset_index()
    Occ17 = grouped_data[(grouped_data['Occupation'] == 17)].reset_index()
    Occ18 = grouped_data[(grouped_data['Occupation'] == 18)].reset_index()
    Occ19 = grouped_data[(grouped_data['Occupation'] == 19)].reset_index()
    Occ20 = grouped_data[(grouped_data['Occupation'] == 20)].reset_index()
    
    
    #print max #products bought by each occupation
    arr = [Occ0, Occ1, Occ2, Occ3, Occ4, Occ5, Occ6, Occ7, Occ8, Occ9, Occ10, Occ11, Occ12, Occ13, Occ14, Occ15, Occ16, Occ17, Occ18, Occ19, Occ20]
    i = 0
    maxprodnum = 0
    occmax = 0
    for o in arr:
        maxValuesindx = o['#Products_bought'].idxmax()
        print("Max Number of products bought by people in Occupation", i, "is", o['#Products_bought'][maxValuesindx], "which belongs to product category", o['Product_Category_1'][maxValuesindx], ".", file=f)
        if o['#Products_bought'][maxValuesindx] > maxprodnum:
            maxprodnum = o['#Products_bought'][maxValuesindx]
            occmax = i
            
        i = i+1
     
    print("The maximum number of products was bought by people in Occupation", occmax, ".", file=f)   
    
    
    #plot them by occupation and product category
    plt.figure(figsize=(30,20))

    plt.xticks(range(1, 21))
    
    plt.scatter(Occ0['Product_Category_1'], Occ0['#Products_bought'], label = 'Occupation_0')
    plt.scatter(Occ1['Product_Category_1'], Occ1['#Products_bought'], label = 'Occupation_1')
    plt.scatter(Occ2['Product_Category_1'], Occ2['#Products_bought'], label = 'Occupation_2')
    plt.scatter(Occ3['Product_Category_1'], Occ3['#Products_bought'], label = 'Occupation_3')
    plt.scatter(Occ4['Product_Category_1'], Occ4['#Products_bought'], label = 'Occupation_4')
    plt.scatter(Occ5['Product_Category_1'], Occ5['#Products_bought'], label = 'Occupation_5')
    plt.scatter(Occ6['Product_Category_1'], Occ6['#Products_bought'], label = 'Occupation_6')
    plt.scatter(Occ7['Product_Category_1'], Occ7['#Products_bought'], label = 'Occupation_7')
    plt.scatter(Occ8['Product_Category_1'], Occ8['#Products_bought'], label = 'Occupation_8')
    plt.scatter(Occ9['Product_Category_1'], Occ9['#Products_bought'], label = 'Occupation_9')
    plt.scatter(Occ10['Product_Category_1'], Occ10['#Products_bought'], label = 'Occupation_10', marker="^")
    plt.scatter(Occ11['Product_Category_1'], Occ11['#Products_bought'], label = 'Occupation_11', marker="^")
    plt.scatter(Occ12['Product_Category_1'], Occ12['#Products_bought'], label = 'Occupation_12', marker="^")
    plt.scatter(Occ13['Product_Category_1'], Occ13['#Products_bought'], label = 'Occupation_13', marker="^")
    plt.scatter(Occ14['Product_Category_1'], Occ14['#Products_bought'], label = 'Occupation_14', marker="^")
    plt.scatter(Occ15['Product_Category_1'], Occ15['#Products_bought'], label = 'Occupation_15', marker="^")
    plt.scatter(Occ16['Product_Category_1'], Occ16['#Products_bought'], label = 'Occupation_16', marker="^")
    plt.scatter(Occ17['Product_Category_1'], Occ17['#Products_bought'], label = 'Occupation_17', marker="^")
    plt.scatter(Occ18['Product_Category_1'], Occ18['#Products_bought'], label = 'Occupation_18', marker="^")
    plt.scatter(Occ19['Product_Category_1'], Occ19['#Products_bought'], label = 'Occupation_19', marker="^")
    plt.scatter(Occ20['Product_Category_1'], Occ20['#Products_bought'], label = 'Occupation_20', marker="x")
    plt.yscale('log')
    #save plot
    plt.legend()
    plt.savefig('Occupation_and_products.svg')
    print("\n", file=f)        
    
def main():
    filename = sys.argv[1]
    data = pd.read_csv(filename)
    #Reference: https://stackoverflow.com/questions/36571560/directing-print-output-to-a-txt-file
    f = open("summary.txt", "w")
     
    gender_and_product_relation(data, f)
    
    martial_and_product_relation(data, f)
    
    occupation_and_product_relation(data, f)
    f.close()
    
if __name__ == '__main__':
     main()