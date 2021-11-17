#!/usr/bin/env python
# coding: utf-8

# # Homework 6, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[ ]:


import pandas as pd
import numpy as np


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[ ]:


#pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", nrows=30000)
df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", nrows=30000,
                na_values=[0, "NA", "UNKNOWN"])
df.head()


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.

# In[327]:


df.shape


# In[328]:


#df.columns.replace('Primary Breed','primary_breed')
df.columns = df.columns.str.replace(' ','_')
#https://www.codegrepper.com/code-examples/python/pandas+remove+spaces+in+the+column+names
df.columns


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[329]:


#Each row in the dataset is animal with a New York license in NYC
# Primay Breed is the main breed of the animal. Some animals will only have a Primary Breed (and no Secondary Breed)
    # and others will have no Primary Breed listed at all. 
# Application Date is a timestamp of when the animal's owner applied for the animals NYC license


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[330]:


# What is the most common breed of animal in the NYC Animal License dataset? What is the most common animal name?
# On average, how long did it take NYC to issue licenses to each of these animals' owners? 
# How many licensed animals in NYC are trained? 
# What is the most common breed of animal that is not spayed or neutered?


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[331]:


df.Primary_Breed.value_counts(ascending=False).head(10).plot.barh(x='Primary_Breed',
                                                                  title ='Most popular breed of dogs', color='#6A186E')


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown

# In[332]:


no_unknown_breed = df.Primary_Breed.replace({
   'Unknown': np.nan
})

no_unknown_breed.value_counts().head(10)


# In[333]:


no_unknown_breed.value_counts(ascending=False).head(10).plot.barh(x='Primary_Breed',
                                                                  title ='Most popular breed of dogs, without Unknown', color='#E884EC')


# ## What are the most popular dog names?

# In[334]:


df.Animal_Name.value_counts(ascending=False).head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[335]:


print(f'377 dogs have the name Max')
df.Animal_Name.str.contains('Max').value_counts()


# In[336]:


print(f'20 dogs have the name Maxwell')
df.Animal_Name.str.contains('Maxwell').value_counts()


# In[337]:


print(f'14 dogs have the name Jessie, yay!')
df.Animal_Name.str.contains('Jessie').value_counts()


# ## What percentage of dogs are guard dogs?
# 
# Check out the documentation for [value counts](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.value_counts.html).

# In[339]:


df.Guard_or_Trained.value_counts(dropna=True).sum()


# In[310]:


(df.Guard_or_Trained.value_counts(dropna=True) / df.Guard_or_Trained.value_counts(dropna=True).sum())*100


# In[340]:


# of animals where training is indicated one way or another, 
    # less than 0.1% of animals are trained


# ## What are the actual numbers?

# In[341]:


df.Guard_or_Trained.value_counts(dropna=True)


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`

# In[342]:


df.Guard_or_Trained.value_counts(dropna=False)


# ## Fill in all of those empty "Guard or Trained" columns with "No"
# 
# Then check your result with another `.value_counts()`

# In[343]:


df.Guard_or_Trained = df.Guard_or_Trained.replace({
   np.NaN : "No"
})

df.Guard_or_Trained.value_counts(dropna=False)


# ## What are the top dog breeds for guard dogs? 

# In[344]:


# df.groupby(by='Primary_Breed')
# df.groupby(by='Primary_Breed').Guard_or_Trained.value_counts(ascending=False).head()
# df.loc[df['Guard_or_Trained'].str.contains('Yes'), 'Gaurd_Dogs'] = 'value if condition is met'
# df.groupby(by='Gaurd_Dogs').Primary_Breed.value_counts.head()
no_unknown_breed[(df.Guard_or_Trained == 'Yes')].value_counts()


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[345]:


df['Birth_Year'] = df['Animal_Birth'].apply(lambda birth: birth.year)
df.Birth_Year


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[346]:


df['Age'] = 2021 - df['Birth_Year']
df.Age.mean()


# # Joining data together

# In[ ]:





# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[347]:


zips = pd.read_csv('zipcodes-neighborhoods.csv', na_values=[0, "NA", "UNKNOWN"])
zips.head()


# In[348]:


merged = df.merge(zips, left_on='Owner_Zip_Code', right_on='zip')
merged.head()
#originally tried this in reverse (left_on='zip'), but it didn't work. 
#I'm confused as to why? 


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?

# In[349]:


merged.Animal_Name[merged.borough == 'Bronx'].value_counts().head(5)


# ## What is the most common dog breed in each of the neighborhoods of NYC?

# In[350]:


merged.groupby(by='neighborhood').Primary_Breed.value_counts()


# ## What breed of dogs are the least likely to be spayed? Male or female?

# In[351]:


merged.Spayed_or_Neut.value_counts(dropna=True)


# In[352]:


#merged.Animal_Name[merged.borough == 'Bronx'].value_counts().head(5)
merged.Primary_Breed[merged.Spayed_or_Neut == 'No'].value_counts().head()
#not sure why the unknows came back or how??


# In[353]:


merged.Animal_Gender.value_counts(dropna=True)
#We could throw away the 3 blanks, but since 3 animals won't make too much of a difference to answering this Q, I'm leaving them in!


# In[354]:


merged.Animal_Gender[merged.Spayed_or_Neut == 'No'].value_counts()
#Females are more likely to be spayed than males


# ## Make a new column called monochrome that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[ ]:


# I can't figure out how exactly to do this question! 


# In[355]:


merged['Monochrome'] = merged.Animal_Dominant_Color.str.contains('Black', 'White', 'Grey')
# merged[merged.Label.str.contains("CHRISTMAS")].Label.value_counts()
# df[df.Other_Race.str.contains("^H[IY]SS?P", na=False)] \
#     .Other_Race \
#     .value_counts()


# ## How many dogs are in each borough? Plot it in a graph.

# In[356]:


boro_dog_count = merged.borough.value_counts(dropna=True)
boro_dog_count


# In[357]:


merged.borough.value_counts().plot(x='Borough', title ='Dog Count By Borough', color='#C14F21', kind='barh')


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[358]:


boro_pop = pd.read_csv('boro_population.csv')
boro_pop.head()


# In[359]:


second_merge = merged.merge(boro_pop, left_on='borough', right_on='borough')
second_merge.head()
#now we need number of dogs per boro and pop per boro


# In[360]:


pop_series = second_merge.groupby(by='borough').population.mean()
pop_series.sort_index()


# In[361]:


boro_dog_count = merged.borough.value_counts(dropna=True)
boro_dog_count.sort_index()


# In[362]:


# I want to 'join' each of the above series 
# so that i can divide dog count by pop 
# or...i wonder if i could create a for-loop here? and put each of these series into a list? 


# series_a = pd.Series([pop_series], name="pop")
# series_b = pd.Series([boro_dog_count], name="dog")

# df2 = pd.concat([series_a, series_b], axis=1)
# #https://www.kite.com/python/answers/how-to-merge-two-pandas-series-into-a-dataframe-in-python
# df2


# In[363]:


pop_series = second_merge.groupby(by='borough').population.mean()
pop_series.sort_index()
pop_series = pop_series.sort_index()

pop_list = []
for pop in pop_series: 
    #print("it works!")
    #omg!
    pop_list.append(pop)
print(pop_series)
pop_list


# In[364]:


boro_dog_count = merged.borough.value_counts(dropna=True)
boro_dog_count.sort_index()
boro_dog_count = boro_dog_count.sort_index()

dog_count_list = []
for count in boro_dog_count: 
    dog_count_list.append(count)
print(boro_dog_count)
dog_count_list


# In[365]:


#products = [a * b for a, b in zip(list1, list2)]
dog_count_list
pop_list

dogs_per_capita = [a / b for a, b in zip(dog_count_list, pop_list)]
dogs_per_capita
#https://www.kite.com/python/answers/how-to-multiply-two-lists-in-python#:~:text=Use%20zip()%20to%20multiply,them%20to%20a%20new%20list.


# In[366]:


print(f'Manhattan has the highest number of dogs per capita!!')


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[372]:


#dogs_per_capita[2]


# ## What percentage of dogs are not guard dogs?

# In[373]:


(df.Guard_or_Trained.value_counts(dropna=True) / df.Guard_or_Trained.value_counts(dropna=True).sum())*100


# In[ ]:


#99.9% of dogs are not gaurd dogs! 


# In[ ]:




