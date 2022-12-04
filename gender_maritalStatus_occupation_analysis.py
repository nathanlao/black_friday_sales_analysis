import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
sns.set_theme()
from scipy import stats

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
    
    #for chi-squared test
    #creates a table with gender as rows and product category as cols and the number of products bought per category as the values
    #print contingency table if confused
    dataset = data[['Product_ID', 'Gender', 'Product_Category_1']]
    grouped_data = dataset.groupby(['Gender', 'Product_Category_1']).count()
    grouped_data.rename(columns = {'Product_ID': '#Products_bought'}, inplace = True)
    grouped_data = grouped_data.reset_index()
    contingency = grouped_data.pivot(index="Gender", columns="Product_Category_1", values="#Products_bought")
    #print p value where is p< 0.05 then the genders affects the categories of products bought
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print("Chi-Squared p-value: ", p, file=f)
    print("\n", file=f)
 

def martial_and_product_relation(data, f):
    print("Martial Status and Product Purchase Relation:", file=f)
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
    
    #for chi-squared test
    #creates a table with marital status as rows and product category as cols and the number of products bought per category as the values
    #print contingency table if confused
    dataset = data[['Product_ID', 'Marital_Status', 'Product_Category_1']]
    grouped_data = dataset.groupby(['Marital_Status', 'Product_Category_1']).count()
    grouped_data.rename(columns = {'Product_ID': '#Products_bought'}, inplace = True)
    grouped_data = grouped_data.reset_index()
    contingency = grouped_data.pivot(index="Marital_Status", columns="Product_Category_1", values="#Products_bought")
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
    fig.savefig('OccupationPurchasesHeatmap.svg')        
    
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