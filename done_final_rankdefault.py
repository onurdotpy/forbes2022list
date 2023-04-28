#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


fb = pd.read_csv("forbes_2022_billionaires.csv")


# In[3]:


fb.columns    #I cannot see columns after 'state' and 'organization', so I will delete unnecessary 4 columns in the end


# In[4]:


fb


# In[5]:


fb = fb.drop("about",axis=1)
fb = fb.drop("bio",axis=1)
fb = fb.drop("numberOfSiblings",axis=1)
fb = fb.drop("residenceMsa",axis=1)

# Alternatively;  fb.loc[:, ["rank","personName", "age" etc etc]]  choses the columns you want to keep.


# In[6]:


fb


# In[7]:


fb = fb.rename(columns={"countryOfCitizenship":"CoC" , "philanthropyScore" : "Pscore"})   #renaming column names


# In[8]:


fb   


# In[9]:


fb["country"].unique()       #just to see what are the country names in the list


# In[10]:


fb["CoC"].unique()


# In[11]:


def cname(value):
    if value == "Turkey":
        return "Türkiye"
    elif value == "United States":
        return "USA"
    elif value == "United Kingdom":
        return "UK"
    else:
        return value


# In[12]:


fb["country"] = fb["country"].apply(cname)


# In[13]:


fb["CoC"] = fb["CoC"].apply(cname)


# In[14]:


fb


# In[15]:


def cleaning(value):
    if value == "M":
        return "Male"
    elif value == "F":
        return "Female"
    else:
        return value


# In[16]:


fb["gender"] = fb["gender"].apply(cleaning)


# In[17]:


fb


# In[18]:


fb[["month","year"]]=fb[["year","month"]]     #exchanging "year" and "month" column locations


# In[19]:


age2 = fb["age"]                           #adding a new duplicated column, so later I will edit new column with lambda function
fb.insert(3, 'age_range', age2)       #index 3 , new column name, from what data storage


# In[20]:


fb


# In[21]:


fb["age_range"] = fb["age_range"].apply(lambda x : "Mature" if x > 30 and x < 60 else ("Young" if x < 30 else "Old"))


# In[22]:


fb


# In[23]:


fb.isnull().sum()     ##shows how many there are missing information (NaN) under each columns


# In[24]:


fb.fillna(fb.median(numeric_only=True), inplace=True)    #filling numerical column's NaN values with whole column's middle value 


# In[51]:


def fill_nan(x):           

    for i in fb.select_dtypes(include='object'):    # checking each column in DataFrame which have object values
        mostfv = x[i].mode().values[0]    # Find the mode (most frequent value) of the column
        print(mostfv)
        fb[i].fillna(value=mostfv, inplace=True)    # Replace missing values with the function

    return fb


# In[52]:


fb = fill_nan(fb)


# In[27]:


fb


# In[28]:


fb.isnull().sum()     #double checking if I still have any NaN values


# In[29]:


fb_gender = fb.groupby("gender")     #grouping them by their gender


# In[30]:


fb_gender["age"].mean()      #shows the richest people's average age between Male and Female


# In[31]:


fb["gender"].value_counts()


# In[32]:


fb_genderbar = fb["gender"].value_counts()


# In[33]:


fb_genderbar.plot.bar()     #showing comparison of amount of gender


# In[34]:


fb_category = fb.groupby("category").size()
fb_category = fb_category.to_frame()          #to see majority of billionares from which category, and shape it into a frame


# In[35]:


fb_category


# In[36]:


fb_category = fb_category.rename(columns={0:"Quantity"}).sort_values(by="Quantity" , ascending=False)  # sort it in order


# In[37]:


fb_category


# In[38]:


grouped1 = fb.groupby("category")["finalWorth"].sum().sort_values()    #to see the Sum of Final Worth by Category

plt.barh(grouped1.index, grouped1.values)
plt.title("Sum of Final Worth by Category")
plt.xlabel("Final Worth")
plt.ylabel("Category")
plt.show()


# In[39]:


grouped2 = fb.groupby("category")["finalWorth"].mean().sort_values(ascending= True)    #to see the Average Worth by Category

plt.barh(grouped2.index, grouped2.values)
plt.title("Average Worth by Category")
plt.xlabel("Worth")
plt.ylabel("Category")
plt.show()


# In[40]:


richestsource = fb.groupby("source")["finalWorth"].sum().sort_values(ascending=False)    # which source have biggest final worth in total
richestsource = richestsource.to_frame()
richestsource


# In[41]:


import seaborn as sns


# In[42]:


fb.head(30)     #let's see the list again


# In[43]:


fig = plt.figure(figsize=(12, 4), dpi=100)           # Top30 - Age and Rank relation graphic
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

x = fb["rank"].head(30)
y = fb["age"].head(30)

ax.plot(x,y, color="green", linewidth=2, marker="o", linestyle="-", label="Age/Rank")

plt.xlabel("Rank")
plt.ylabel("Age")

ax.legend()


# In[44]:


sns.histplot(fb["age"])    #this graph shows what is most of the richest people's age range


# In[45]:


fb_youngest = fb.sort_values(by="age")            #storing the youngest 10 richest
fb_youngest.head(10)                           


# In[46]:


sns.barplot(y=fb_youngest["personName"][:10], x = fb_youngest["finalWorth"][:10])   #printing out their graph by Name and Worth


# In[47]:


fb_oldest = fb.sort_values(by="age", ascending= False)    #storing the oldest 10 richest
fb_oldest.head(10)


# In[48]:


sns.barplot(y=fb_oldest["personName"][:10], x = fb_oldest["finalWorth"][:10])   #printing out their graph by Name and Worth


# In[49]:


fb_mostgenerous = fb.sort_values(by=["Pscore"], ascending=[False]).head(20)
fb_mostgenerous = pd.DataFrame(fb_mostgenerous, columns=["personName", "age", "finalWorth", "source" , "Pscore"])
fb_mostgenerous


# In[50]:


#end

