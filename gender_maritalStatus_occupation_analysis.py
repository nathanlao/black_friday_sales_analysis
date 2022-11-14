import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def gender_and_product_relation(data):
    #separate females and males data
    f_purchases = data[(data['Gender'] == 'F')]
    m_purchases = data[(data['Gender'] == 'M')]
    #print the amount of products purchased by females vs males
    print("From our dataset we can see Females bought ", f_purchases['Product_ID'].count(), "and Males bought ", m_purchases['Product_ID'].count(), "products")
    
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
    print("The most popular product for females had Product_ID: ", f_maxid, "and belonged to primary category", f_purchases[(f_purchases['Product_ID'] == f_maxid)].Product_Category_1.values[0], ".", f_product_id[f_maxid], "purchases of this product was made by females.")
    print("The most popular product for males had Product_ID: ", m_maxid, "and belonged to primary category", m_purchases[(m_purchases['Product_ID'] == m_maxid)].Product_Category_1.values[0], ".", m_product_id[m_maxid], "purchases of this product was made by males.")

    #plot the amount of products purchased per category for each gender
    xlabels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    plt.figure(figsize=(15,4))

    #plot the female purchases
    plt.subplot(1,2,1)
    plt.title("Female product purchases")
    plt.xlabel("Product_Category#")
    plt.xticks(f_products.index, xlabels, rotation='vertical')
    plt.ylabel("# of product purchased in each category")
    plt.yscale('log') #chose log scale since if I plot directly it seems like category 9 and 17 have 0 purtchases since its so low
    plt.bar(f_products.index, f_products)

    #plot the male purchases
    plt.subplot(1,2,2)
    plt.title("Male product purchases")
    plt.xlabel("Product_Category#")
    plt.xticks(m_products.index, xlabels, rotation='vertical')
    plt.ylabel("# of product purchased in each category")
    plt.yscale('log') #chose log scale since if I plot directly it seems like category 9 and 17 have 0 purtchases since its so low
    plt.bar(m_products.index, m_products)
    #plt.show()
    plt.savefig('gender_and_products.svg')
    
    
def main():
    filename = sys.argv[1]
    data = pd.read_csv(filename)
    gender_and_product_relation(data)
    
if __name__ == '__main__':
     main()
