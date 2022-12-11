# Black Friday Sales
This project analyzes Black Friday sales data to better understand the product purchase patterns of customers on Black Friday. There are 3 parts to this project:

**Part 1**: analysis on how age, gender, and other categories affect one’s product consumption

**Part 2**: analysis on which products specifically get purchased more by certain categories/types of customers

**Part 3**: machine learning to predict the future product consumption during Black Fridays for each category

## Environment Setup
Install the following on your machine:

* Git
* Python 

Make sure you have properly set up an SSH key. Then clone the repository to your machine:
```
git clone git@github.sfu.ca:gla93/CMPT353_group_project.git
```

## Required Libraries
* pandas
* numpy
* scipy
* scikit-learn
* matplotlib
* seaborn

## How to Run
**Note:** the .py files do not rely on each other and can be executed in any order

Running Part 1:
```
python3 part1_consumption.py black_friday_sales_data.csv
```

Running Part 2:
```
python3 part2_popularity.py black_friday_sales_data.csv
```

Running Part 3:
```
python3 part3_ML_classification.py black_friday_sales_data.csv
```

## Files Produced/Expected
After running Part 1, the following files should be produced in a `PartI_Output` folder:

* `age_and_products.svg`
* `age_and_total_products.svg`
* `City_and_products.svg`
* `gender_and_products.svg`
* `Martial_status_and_products.svg`
* `OccupationPurchasesHeatmap.svg`
* `city_purchases.csv`
* `Gender_purchases.csv`
* `Marital_status_purchases.csv`
* `Occupation_purchases.csv`
* `summary.txt`

After running Part 2, the following files should be produced in a `Part2_Output` folder:

* `combined_female_age_popularity.svg`
* `combined_female_marital_status_popularity.svg`
* `combined_male_age_popularity.svg`
* `combined_male_marital_status_popularity.svg`
* `only_age_popularity.svg`
* `only_city_popularity.svg`
* `only_gender_popularity.svg`
* `only_marital_status_popularity.svg`
* `only_occupation_popularity.svg`
* `popularity_summaries.txt`

After running Part 3, the following file should be produced in a `Part3_Output` folder:

* `summary.txt`

## Resource Links
Dataset: https://www.kaggle.com/datasets/rishikeshkonapure/black-friday-sales-eda

## Contributors
* gla93
* ana82
* dag7
