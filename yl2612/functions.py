import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_data_q2(df):
    '''
    This function clean up the data as required by question 2.
    '''
    clean_df = df[['CAMIS', 'BORO', 'GRADE', 'GRADE DATE']] #select the columns that will be used for assessment
    clean_df = clean_df.dropna() #remove rows with missing data
    clean_df = clean_df[clean_df.GRADE != 'Not Yet Graded'] #remove rows having 'Not yet Graded' in the 'GRADE' column
    clean_df = clean_df[clean_df.GRADE != 'P']  #remove rows having 'P' in the 'GRADE' column
    clean_df = clean_df[clean_df.GRADE != 'Z']  #remove rows having 'Z' in the 'GRADE' column
    clean_df = clean_df.drop_duplicates() #drop duplicated rows
    clean_df['GRADE DATE'] = pd.to_datetime(clean_df['GRADE DATE']) #convert string to date for the 'GRADE DATE' column
    clean_df = clean_df.set_index('CAMIS') #set the row labels using the 'CAMIS' column
    return clean_df


def test_grades(grade_list):
    '''
    Take a list of grades sorted in date order,
    returns 1 if the median grade after the first graded date, i.e., median grade excepting the first grade, is bigger than the first grade,
    returns -1 if it is smaller than the first grade,
    and returns 0 if they are the same.
    '''
    grade_num = {'A':3, 'B':2, 'C':1} # create a dictionary that map A,B,C to 3,2,1, respectively
    grade_list_num = [grade_num[grade] for grade in grade_list] #create a new list using 1,2,3 to represent A,B,C.
    
    if len(grade_list)==1: #returns 0 if there is only one grade in the list
        return 0
    if grade_list_num[0] > np.median(grade_list_num[1:]):
        return -1
    elif grade_list_num[0] < np.median(grade_list_num[1:]):
        return 1
    else:
        return 0


def test_restaurant_grades(df,camis_id):
    '''
    Examine if the grade for a restaurant is improving.
    Return 1 if it is improving, -1 if it is declining, 0 if it stays the same.
    '''  
    collect_grades = df.GRADE[df.index==camis_id] #select grades having the same camis_id
    assess_quality = test_grades(collect_grades)
    return assess_quality


def get_sum(df):
    '''
    This function calculates the sum of improvement.
    '''
    collect_unique_ids = df.index.unique() #collect the ids
    compute_sum = 0
    for unique_id in collect_unique_ids:
        compute_sum += test_restaurant_grades(df, unique_id)
    return compute_sum


def process_data_q5(df):
    '''
    Generate a data frame for grade, with row index as 'GRADE DATE' and column index as 'CAMIS' id.
    '''
    li_date=[]
    unique_date = df['GRADE DATE'].unique() #select the unique dates
    for date in unique_date:
        date_df = df[df['GRADE DATE'] == date] #create a data frame for each unique date
        create_dict = dict(zip(date_df.index, date_df['GRADE']))
        li_date.append(create_dict) #create a list of dictionaries
        
    date_grade_id = pd.DataFrame(data=li_date) #change the list to a data frame
    date_grade_id = date_grade_id.set_index(unique_date)
    date_grade_id = date_grade_id.fillna(method='ffill') #fill missing with the last observed grade in each column
    
    return date_grade_id


def grade_graph(df,area):
    '''
    Generate a graph that shows the total number of restaurants for each grade over time.
    '''
    count_grades = df.apply(pd.Series.value_counts, axis=1) #count the number of grades at different dates
    uncapitalized_area = area.lower()
    plt.figure()
    count_grades.plot()
    plt.title('grade improvement in {}'.format(uncapitalized_area))
    plt.savefig('grade_improvement_{}.pdf'.format(uncapitalized_area.split(' ')[0]))
    
    
def process_data_q6(df):
    '''
    Clean up the data for question 6.
    Return a data frame with cuisine description as row label and the number of restaurants as column label
    '''   
    cuisine_df = df[['CAMIS', 'CUISINE DESCRIPTION']] #select columns that will be used for q6
    cuisine_df = cuisine_df.dropna()
    cuisine_df = cuisine_df.drop_duplicates()
    cuisine_df = cuisine_df.set_index('CAMIS')
    count_num = cuisine_df.apply(pd.Series.value_counts, axis=0) #count the number of cuisines
    count_num.columns =['Count'] #change the column name
    count_num = count_num.sort('Count',ascending=False) #sort the data frame with the largest count on top.
    return count_num

def selector(df, num_range):
    '''
    Select the data above a certain number range.
    Return a data frame with the number of restarurants larger than the specfied number range
    '''
    new_df = df[df['Count'] > num_range]#create a new df with 'Count' larger than the specfied number range
    return new_df


def bar_grade(df):
    '''
    Create a bar plot for q6 that shows the number of restaurants in different cuisines.
    '''
    plt.figure(figsize=(10, 8))
    df.plot(y='Count', kind='bar',rot=45,fontsize=9)#create a bar plot
    plt.title('Number of restaurants in different cuisines')
    plt.savefig('Number_of_restaurants_in_different_cuisines.pdf')