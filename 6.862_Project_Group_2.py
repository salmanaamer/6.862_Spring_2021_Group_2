# -*- coding: utf-8 -*-
"""ML Data Cleaning Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/salmanaamer/d5e1ad9631d88ea3efbcd310163295f9/ml-data-cleaning-project.ipynb
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from mlxtend.preprocessing import standardize

data_raw = pd.read_csv("/content/PAKDD2010_Modeling_Data.txt", sep = '\t', encoding = 'mac_roman', header=None)
data_raw

col_names = ["ID_CLIENT", "CLERK_TYPE", "PAYMENT_DAY", "APPLICATION_SUBMISSION_TYPE", "QUANT_ADDITIONAL_CARDS",
             "POSTAL_ADDRESS_TYPE","SEX","MARITAL_STATUS","QUANT_DEPENDANTS","EDUCATION_LEVEL","STATE_OF_BIRTH",
             "CITY_OF_BIRTH","NACIONALITY","RESIDENCIAL_STATE","RESIDENCIAL_CITY","RESIDENCIAL_BOROUGH",
             "FLAG_RESIDENCIAL_PHONE", "RESIDENCIAL_PHONE_AREA_CODE", "RESIDENCE_TYPE", "MONTHS_IN_RESIDENCE",
             "FLAG_MOBILE_PHONE","FLAG_EMAIL","PERSONAL_MONTHLY_INCOME","OTHER_INCOMES", "FLAG_VISA","FLAG_MASTERCARD",
             "FLAG_DINERS","FLAG_AMERICAN_EXPRESS","FLAG_OTHER_CARDS","QUANT_BANKING_ACCOUNTS","QUANT_SPECIAL_BANKING_ACCOUNTS",
             "PERSONAL_ASSETS_VALUE","QUANT_CARS","COMPANY","PROFESSIONAL_STATE","PROFESSIONAL_CITY","PROFESSIONAL_BOROUGH",
             "FLAG_PROFESSIONAL_PHONE","PROFESSIONAL_PHONE_AREA_CODE","MONTHS_IN_THE_JOB","PROFESSION_CODE","OCCUPATION_TYPE",
             "MATE_PROFESSION_CODE","MATE_EDUCATION_LEVEL","FLAG_HOME_ADDRESS_DOCUMENT","FLAG_RG","FLAG_CPF","FLAG_INCOME_PROOF",
             "PRODUCT","FLAG_ACSP_RECORD", "AGE", "RESIDENCIAL_ZIP_3","PROFESSIONAL_ZIP_3", "TARGET_LABEL"]

data_raw.columns = col_names
data_raw

"""# 1) Variables with known NaN's"""

#Checking which columns contain "NaN" values
col_with_nan = []
for col in data_raw:
  if data_raw[col].isnull().values.any():
    col_with_nan.append(col)

col_with_nan

"""Another issue we are seeing here is that EDUCATION_LEVEL has no explanatory power as seen as below, so MATE_EDUCATION_LEVEL might me a good substitute for it"""

count = 0
for row in range(50000):
  if data_raw.loc[row, "EDUCATION_LEVEL"] == 0:
    count = count + 1

count

"""Let us first consider MATE_EDUCATION_LEVEL to see the number of missing values."""

nan_count = 0
nan_idx = []
ed_level = []
for row in range(50000):
  if math.isnan(data_raw.loc[row, "MATE_EDUCATION_LEVEL"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    ed_level.append(data_raw.loc[row, "MATE_EDUCATION_LEVEL"])

nan_count

"""There are a lot of missing observations, namely 32338. We need to see if we can potentially replace those observations maybe using median/mean. Let us look at the statistics of current observations."""

np.mean(ed_level)

np.median(ed_level)

ed_level.count(0.0)

ed_level.count(0.0)/len(ed_level)

"""We can also keep the variable if the values with different education level may be extremely significant, but we will have to make a judgement call on how to handle the missing observations. The values are close to zero, we may consider instead to drop the column altogether since we see about 90.56% of observations equal to 0.

Let us consider RESIDENCE_TYPE as a variable now
"""

nan_count = 0
nan_idx = []
res_type = []
for row in range(50000):
  if math.isnan(data_raw.loc[row, "RESIDENCE_TYPE"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    res_type.append(data_raw.loc[row, "RESIDENCE_TYPE"])

nan_count

"""Ideally we do not want to omit the observations as it would reduce our predictive power. As such, we will instead replace with the median value of the residence type"""

np.median(res_type)

print("Number of 0.0:")
print(res_type.count(0.0))
print("Number of 1.0:")
print(res_type.count(1.0))
print("Number of 2.0:")
print(res_type.count(2.0))
print("Number of 3.0:")
print(res_type.count(3.0))
print("Number of 4.0:")
print(res_type.count(4.0))
print("Number of 5.0:")
print(res_type.count(5.0))

"""Let us know consider the MONTHS_IN_RESIDENCE variable"""

nan_count = 0
nan_idx = []
mir_nums = []
for row in range(50000):
  if math.isnan(data_raw.loc[row, "MONTHS_IN_RESIDENCE"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    mir_nums.append(data_raw.loc[row, "MONTHS_IN_RESIDENCE"])

nan_count

_ = plt.figure(figsize=(10,10))
_ = plt.hist(mir_nums, bins = 100)

"""We will replace the missing values by the median value as this value will be less sensitive to outliers and will be more reasonable.

We can now consider the PROFESSIONAL_CITY variable and see how we will handle NaN's in this case.
"""

nan_count = 0
nan_idx = []
prof_cit = []
for row in range(50000):
  if pd.isna(data_raw.loc[row, "PROFESSIONAL_CITY"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    prof_cit.append(data_raw.loc[row, "PROFESSIONAL_CITY"])

nan_count

"""With such a large amount of NaN observations, and with no potential replaceable value, it is better for us to drop the column altogether.

We can now look at PROFESSIONAL_BOROUGH which may have less NaN observations than PROFESSIONAL_CITY.
"""

nan_count = 0
nan_idx = []
prof_bor = []
for row in range(50000):
  if pd.isna(data_raw.loc[row, "PROFESSIONAL_BOROUGH"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    prof_bor.append(data_raw.loc[row, "PROFESSIONAL_BOROUGH"])

nan_count

"""The number of NaN is exactly the same for the PROFESSIONAL_CITY variable, and so we can simply drop the PROFESSIONAL_BOROUGH.

Let's now consider PROFESSION_CODE and see how we will treat the NaN values
"""

nan_count = 0
nan_idx = []
prof_code = []
for row in range(50000):
  if math.isnan(data_raw.loc[row, "PROFESSION_CODE"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    prof_code.append(data_raw.loc[row, "PROFESSION_CODE"])

nan_count

"""The number of missing values is quite moderate, we will see first of all what is the distribution of the categories"""

_ = plt.figure(figsize=(10,10))
_ = plt.hist(prof_code, bins = 19)

len(set(prof_code))

"""To avoid overfitting, we will likely create an indicator random variable for the most frequent category/categories.

Now let's consider the OCCUPATION_TYPE variable. We do not have a lot of information about the occupation type of the person applying, nor do we know much about how it differs from the PROFESSION_CODE
"""

nan_count = 0
nan_idx = []
occ_type = []
for row in range(50000):
  if math.isnan(data_raw.loc[row, "OCCUPATION_TYPE"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    occ_type.append(data_raw.loc[row, "OCCUPATION_TYPE"])

nan_count

_ = plt.hist(occ_type)

"""The number of missing observations is quite close to the number of missing observations for PROFESSION_CODE. Because we believe there could be a significant amount of correlation with PROFESSION_CODE, this variable will likely not add superior explanatory power. We may consider dropping the column altogether depending on what we choose to do with the PROFESSION_CODE variable. We also do not want to extrapolate on a variable for which we have no tangible information on what it means.

Let's now evaluate the MATE_PROFESSION_CODE.
"""

nan_count = 0
nan_idx = []
mate_prof_code = []
for row in range(50000):
  if math.isnan(data_raw.loc[row, "MATE_PROFESSION_CODE"]):
    nan_count = nan_count + 1
    nan_idx.append(row)
  else:
    mate_prof_code.append(data_raw.loc[row, "MATE_PROFESSION_CODE"])

nan_count

len(set(mate_prof_code))

"""The number of missing observations is quite large, but we could still accommodate it by adding indicator random variables for frequent variable and leave the missing observation as being an infrequent profession code for the partner of the person who filed the application.

## 2) Variables with Bad Values

Let us consider SEX as a variable now, this variable will be critical to our analysis, as such we must deal with precaution while handling potential values that are not incorrectly inputted.
"""

m_count = 0
f_count = 0
other_count = 0
other_list = []
for i in range(50000):
  if data_raw.loc[i, "SEX"] == "M":
    m_count += 1
  elif data_raw.loc[i, "SEX"] == "F":
    f_count += 1
  else:
    other_count += 1
    other_list.append(data_raw.loc[i,"SEX"])

#NUMBER OF MALES
m_count

#NUMBER OF FEMALES
f_count

#NUMBER OF OTHER SEXES
other_count

#LIST OF INPUTS IN THE OTHER SEXES
other_list

"""We see that there are about 65 observations that have "N" or " " as their inputs, which likely point towards values that have been incorrectly inputted. We do not want to replace those observations towards Male or Female, and as such we can safely drop those 65 observations.

# 3) Cleaning
"""

data_nans_fixed = pd.DataFrame(data_raw)
other_nan_values = []
for row in range(len(data_nans_fixed)):
    for col in data_nans_fixed.columns:
        if pd.isnull(data_nans_fixed.loc[row, col]):
            other_nan_values.append(data_nans_fixed.loc[row, col])
            data_nans_fixed.loc[row, col] = float('nan')
        if data_nans_fixed.loc[row, col] == ' ':
            data_nans_fixed.loc[row, col] = float('nan')
for row in range(len(data_nans_fixed)):
    if data_nans_fixed.loc[row, 'SEX'] == 'N':
        data_nans_fixed.loc[row, 'SEX'] = float('nan')

#data_clean = pd.DataFrame(data_raw)
#data_clean
data_nans_fixed

#MONTHS_IN_RESIDENCE
mir_med = np.median(mir_nums)
data_nans_fixed["MONTHS_IN_RESIDENCE"] = data_nans_fixed["MONTHS_IN_RESIDENCE"].replace(np.nan, mir_med)
data_nans_fixed["MONTHS_IN_RESIDENCE"]

#COMPANY
data_nans_fixed["COMPANY"] = data_nans_fixed["COMPANY"].replace("N", 0)
data_nans_fixed["COMPANY"] = data_nans_fixed["COMPANY"].replace("Y", 1)
data_nans_fixed["COMPANY"]

#PRODUCT
set(data_nans_fixed["PRODUCT"])

prod_list = list(data_nans_fixed["PRODUCT"])
list_prod_one = [1 if x==1 else 0 for x in prod_list]
list_prod_two = [1 if x==2 else 0 for x in prod_list]
list_prod_seven = [1 if x==7 else 0 for x in prod_list]

data_nans_fixed["PRODUCT_1"] = pd.Series(list_prod_one)
data_nans_fixed["PRODUCT_2"] = pd.Series(list_prod_two)
data_nans_fixed["PRODUCT_7"] = pd.Series(list_prod_seven)
data_nans_fixed

#FLAG_CREDIT_CARD
data_nans_fixed["FLAG_CREDIT_CARD"] = data_nans_fixed["FLAG_VISA"] | data_nans_fixed["FLAG_DINERS"] | data_nans_fixed["FLAG_MASTERCARD"] | data_nans_fixed["FLAG_AMERICAN_EXPRESS"] | data_nans_fixed["FLAG_OTHER_CARDS"]
data_nans_fixed["FLAG_CREDIT_CARD"]

#checking for invalid values of FLAG_PROFESSIONAL_PHONE
count_prof_phone_nan = 0
for row in range(len(data_nans_fixed)):
    if data_nans_fixed.loc[row, 'FLAG_PROFESSIONAL_PHONE'] not in ['N','Y']:
        data_nans_fixed.loc[row, 'FLAG_PROFESSIONAL_PHONE'] = float('nan')
        count_prof_phone_nan += 1

set(data_nans_fixed["FLAG_PROFESSIONAL_PHONE"])

#converting N,Y to 0,1 for FLAG_PROFESSIONAL PHONE
data_nans_fixed["FLAG_PROFESSIONAL_PHONE"] = data_nans_fixed["FLAG_PROFESSIONAL_PHONE"].replace("N",0)
data_nans_fixed["FLAG_PROFESSIONAL_PHONE"] = data_nans_fixed["FLAG_PROFESSIONAL_PHONE"].replace("Y",1)
data_nans_fixed["FLAG_PROFESSIONAL_PHONE"]

#converting N,Y to 0,1 for FLAG_PROFESSIONAL PHONE
data_nans_fixed["FLAG_RESIDENCIAL_PHONE"] = data_nans_fixed["FLAG_RESIDENCIAL_PHONE"].replace("N",0)
data_nans_fixed["FLAG_RESIDENCIAL_PHONE"] = data_nans_fixed["FLAG_RESIDENCIAL_PHONE"].replace("Y",1)
data_nans_fixed["FLAG_RESIDENCIAL_PHONE"]

#checking for invalid values of FLAG_MOBILE_PHONE
count_mob_phone_Y = 0
for row in range(len(data_nans_fixed)):
    if data_nans_fixed.loc[row, 'FLAG_MOBILE_PHONE'] != 'N':
        count_mob_phone_Y += 1

count_mob_phone_Y

data_nans_fixed['TOTAL_INCOME'] = data_nans_fixed['PERSONAL_MONTHLY_INCOME'] + data_nans_fixed['OTHER_INCOMES']
data_nans_fixed['TOTAL_INCOME_STD'] = standardize(data_nans_fixed['TOTAL_INCOME'])

data_nans_fixed["TOTAL_INCOME"]

data_nans_fixed["TOTAL_INCOME_STD"]

res_type_prod_list = list(data_nans_fixed["RESIDENCE_TYPE"])
res_list_prod_zero = [1 if x==0 else 0 for x in res_type_prod_list]
res_list_prod_one = [1 if x==1 else 0 for x in res_type_prod_list]
res_list_prod_two = [1 if x==2 else 0 for x in res_type_prod_list]
res_list_prod_three = [1 if x==3 else 0 for x in res_type_prod_list]
res_list_prod_four = [1 if x==4 else 0 for x in res_type_prod_list]
res_list_prod_five = [1 if x==5 else 0 for x in res_type_prod_list]

#One-Hot encode Residence Type
data_nans_fixed["RESIDENCE_TYPE_0"] = pd.Series(res_list_prod_zero)
data_nans_fixed["RESIDENCE_TYPE_1"] = pd.Series(res_list_prod_one)
data_nans_fixed["RESIDENCE_TYPE_2"] = pd.Series(res_list_prod_two)
data_nans_fixed["RESIDENCE_TYPE_3"] = pd.Series(res_list_prod_three)
data_nans_fixed["RESIDENCE_TYPE_4"] = pd.Series(res_list_prod_four)
data_nans_fixed["RESIDENCE_TYPE_5"] = pd.Series(res_list_prod_five)
data_nans_fixed

payday_prod_list = list(data_nans_fixed["PAYMENT_DAY"])
payday_prod_one = [1 if x==1 else 0 for x in payday_prod_list]
payday_prod_five = [1 if x==5 else 0 for x in payday_prod_list]
payday_prod_ten = [1 if x==10 else 0 for x in payday_prod_list]
payday_prod_fifteen = [1 if x==15 else 0 for x in payday_prod_list]
payday_prod_twenty = [1 if x==20 else 0 for x in payday_prod_list]
payday_prod_twentyfive = [1 if x==25 else 0 for x in payday_prod_list]

#One-Hot Encode Payment Day
data_nans_fixed["PAYMENT_DAY_1"] = pd.Series(payday_prod_one)
data_nans_fixed["PAYMENT_DAY_5"] = pd.Series(payday_prod_five)
data_nans_fixed["PAYMENT_DAY_10"] = pd.Series(payday_prod_ten)
data_nans_fixed["PAYMENT_DAY_15"] = pd.Series(payday_prod_fifteen)
data_nans_fixed["PAYMENT_DAY_20"] = pd.Series(payday_prod_twenty)
data_nans_fixed["PAYMENT_DAY_25"] = pd.Series(payday_prod_twentyfive)
data_nans_fixed

#Encode Postal Address Type (1 --> 1, 2 --> 0)
data_nans_fixed["POSTAL_ADDRESS_TYPE"] = data_nans_fixed["POSTAL_ADDRESS_TYPE"].replace(2,0)
data_nans_fixed["POSTAL_ADDRESS_TYPE"]

#Encode SEX (F --> 1, M --> 0)
data_nans_fixed["SEX"] = data_nans_fixed["SEX"].replace("M",int(0))
data_nans_fixed["SEX"] = data_nans_fixed["SEX"].replace("F",int(1))
data_nans_fixed["SEX"]

#Check Number of Categories for Marital Status
set(data_nans_fixed["MARITAL_STATUS"])

marital_prod_list = list(data_nans_fixed["MARITAL_STATUS"])
marital_prod_one = [1 if x== 1 else 0 for x in marital_prod_list]
marital_prod_two = [1 if x== 2 else 0 for x in marital_prod_list]
marital_prod_three = [1 if x== 3 else 0 for x in marital_prod_list]
marital_prod_four= [1 if x== 4 else 0 for x in marital_prod_list]
marital_prod_five = [1 if x== 5 else 0 for x in marital_prod_list]
marital_prod_six = [1 if x== 6 else 0 for x in marital_prod_list]
marital_prod_seven = [1 if x== 7 else 0 for x in marital_prod_list]

data_nans_fixed["MARITAL_STATUS_1"] = pd.Series(marital_prod_one)
data_nans_fixed["MARITAL_STATUS_2"] = pd.Series(marital_prod_two)
data_nans_fixed["MARITAL_STATUS_3"] = pd.Series(marital_prod_three)
data_nans_fixed["MARITAL_STATUS_4"] = pd.Series(marital_prod_four)
data_nans_fixed["MARITAL_STATUS_5"] = pd.Series(marital_prod_five)
data_nans_fixed["MARITAL_STATUS_6"] = pd.Series(marital_prod_six)
data_nans_fixed["MARITAL_STATUS_7"] = pd.Series(marital_prod_seven)

data_nans_fixed

#Finding Lowest AGE values --> will drop 3 values: 6, 7, 14
np.sort(list(data_nans_fixed["AGE"]))[0:10]

_ = plt.hist(data_nans_fixed["AGE"])

age_list = list(data_nans_fixed["AGE"])
age_one = [1 if x >= 17 and x <= 25 else 0 for x in age_list]
age_two = [1 if x > 25 and x <= 35 else 0 for x in age_list]
age_three = [1 if x > 35 and x <= 45 else 0 for x in age_list]
age_four= [1 if x > 45 and x <= 55 else 0 for x in age_list]
age_five = [1 if x > 55 and x <= 75 else 0 for x in age_list]
age_six = [1 if x > 75 else 0 for x in age_list]

data_nans_fixed["AGE_17_25"] = pd.Series(age_one)
data_nans_fixed["AGE_26_35"] = pd.Series(age_two)
data_nans_fixed["AGE_36_45"] = pd.Series(age_three)
data_nans_fixed["AGE_46_55"] = pd.Series(age_four)
data_nans_fixed["AGE_56_75"] = pd.Series(age_five)
data_nans_fixed["AGE_76_PLUS"] = pd.Series(age_six)

"""# Dropping NaNs"""

col_with_nan = []
for col in data_nans_fixed:
  if data_nans_fixed[col].isnull().values.any():
    col_with_nan.append(col)

col_with_nan

#SEX - 65 Observation Dropped
data_nans_dropped = pd.DataFrame(data_nans_fixed)
data_nans_dropped = data_nans_dropped.dropna(axis = 0, subset = ["SEX"])
data_nans_dropped["SEX"] = data_nans_dropped["SEX"].astype('int')

#EDUCATION_LEVEL - No explanatory Power (ALL Zeroes)
#MATE_EDUCATION_LEVEL - 32,000 Missing Observations
data_nans_dropped = data_nans_dropped.drop(labels = ["EDUCATION_LEVEL", "MATE_EDUCATION_LEVEL"], axis = 1)

data_nans_dropped = data_nans_dropped.dropna(axis = 0, subset = ["RESIDENCE_TYPE"])

#Drop RESIDENCE_TYPE (Since we one-hot encoded it)
data_nans_dropped = data_nans_dropped.drop(labels = ["RESIDENCE_TYPE"], axis = 1)

#Check Missing Observations in Application Submission Type
sum([x == '0' for x in data_nans_dropped["APPLICATION_SUBMISSION_TYPE"]])

#DROP APPLICATION_SUBMISSION_TYPE
data_nans_dropped = data_nans_dropped.drop(labels = ["APPLICATION_SUBMISSION_TYPE"], axis = 1)

#DROP CLERK TYPE (NO INFO)
data_nans_dropped = data_nans_dropped.drop(labels = ["CLERK_TYPE"], axis = 1)

set(data_nans_dropped["QUANT_ADDITIONAL_CARDS"])

#DROP QUANT_ADDITIONAL_CARDS (ALL ZEROES)
data_nans_dropped = data_nans_dropped.drop(labels = ["QUANT_ADDITIONAL_CARDS"], axis = 1)

#DROP PAYMENT_DAY (ALREADY ONE-HOT ENCODED)
data_nans_dropped = data_nans_dropped.drop(labels = ["PAYMENT_DAY"], axis = 1)

#Drop Observations where Marital Status = 0, only 202 observations
data_nans_dropped["MARITAL_STATUS"] = data_nans_dropped["MARITAL_STATUS"].replace(0, np.nan)
data_nans_dropped = data_nans_dropped.dropna(axis = 0, subset = ["MARITAL_STATUS"])

data_nans_dropped = data_nans_dropped.drop(labels = ["MARITAL_STATUS"], axis = 1)

#Drop Nationality as a variable (because no clear interpretation of encoding)
data_nans_dropped = data_nans_dropped.drop(labels = ["NACIONALITY"], axis = 1)

#Check number of NaN's in RESIDENCIAL_PHONE_AREA_CODE (7917)
sum(data_nans_dropped["RESIDENCIAL_PHONE_AREA_CODE"].isnull())

#Drop RESIDENCIAL_PHONE_AREA_CODE
data_nans_dropped = data_nans_dropped.drop(labels = ["RESIDENCIAL_PHONE_AREA_CODE"], axis = 1)

#Drop Flag Mobile Phone (all N)
data_nans_dropped = data_nans_dropped.drop(labels = ["FLAG_MOBILE_PHONE"], axis = 1)

#Check Quant Banking Accounts and Quant Special Banking Accounts
sum(data_nans_dropped["QUANT_SPECIAL_BANKING_ACCOUNTS"] != data_nans_dropped["QUANT_BANKING_ACCOUNTS"])

#Check Quant Special Banking Accounts
data_nans_dropped = data_nans_dropped.drop(labels = ["QUANT_SPECIAL_BANKING_ACCOUNTS"], axis = 1)

#Count the number of observations with 0 value
sum([x == 0.0 for x in data_nans_dropped["PERSONAL_ASSETS_VALUE"]])

#Drop Personal Assets Value
data_nans_dropped = data_nans_dropped.drop(labels = ["PERSONAL_ASSETS_VALUE"], axis = 1)

#Count Number of NaNs in PROFESSIONAL_STATE
sum(data_nans_dropped["PROFESSIONAL_STATE"].isnull())

#Drop PROFESSIONAL_STATE
data_nans_dropped = data_nans_dropped.drop(labels = ["PROFESSIONAL_STATE"], axis = 1)

#Count Number of NaNs in PROFESSIONAL_CITY
sum(data_nans_dropped["PROFESSIONAL_CITY"].isnull())

#Drop PROFESSIONAL_STATE
data_nans_dropped = data_nans_dropped.drop(labels = ["PROFESSIONAL_CITY"], axis = 1)

#Count Number of NaNs in PROFESSIONAL_BOROUGH
sum(data_nans_dropped["PROFESSIONAL_BOROUGH"].isnull())

#Drop PROFESSIONAL_BOROUGH
data_nans_dropped = data_nans_dropped.drop(labels = ["PROFESSIONAL_BOROUGH"], axis = 1)

#Count NUmber of NaNs in PROFESSIONAL_PHONE_AREA_CODE
sum(data_nans_dropped["PROFESSIONAL_PHONE_AREA_CODE"].isnull())

#Count NUmber of NaNs in PROFESSIONAL_PHONE_AREA_CODE
data_nans_dropped = data_nans_dropped.drop(labels = ["PROFESSIONAL_PHONE_AREA_CODE"], axis = 1)

#Count NUmber of NaNs in MATE_PROFESSION_CODE
sum(data_nans_dropped["MATE_PROFESSION_CODE"].isnull())

#Drop MATE_PROFESSION_CODE
data_nans_dropped = data_nans_dropped.drop(labels = ["MATE_PROFESSION_CODE"], axis = 1)

#Count NUmber of NaNs in FLAG_HOME_ADDRESS_DOCUMENT
sum([x == 0 for x in data_nans_dropped["FLAG_HOME_ADDRESS_DOCUMENT"]])

#Count NUmber of NaNs in FLAG_RG
sum([x == 0 for x in data_nans_dropped["FLAG_RG"]])

#Drop FLAG_HOME_ADDRESS_DOCUMENT
data_nans_dropped = data_nans_dropped.drop(labels = ["FLAG_HOME_ADDRESS_DOCUMENT"], axis = 1)

#Drop FLAG_HOME_ADDRESS_DOCUMENT
data_nans_dropped = data_nans_dropped.drop(labels = ["FLAG_RG"], axis = 1)

#Count NUmber of NaNs in FLAG_CPF
sum([x == 0 for x in data_nans_dropped["FLAG_CPF"]])

#Count NUmber of NaNs in FLAG_INCOME_PROOF
sum([x == 0 for x in data_nans_dropped["FLAG_INCOME_PROOF"]])

#Drop FLAG_CPF
data_nans_dropped = data_nans_dropped.drop(labels = ["FLAG_CPF"], axis = 1)

#Drop FLAG_INCOME_PROOF
data_nans_dropped = data_nans_dropped.drop(labels = ["FLAG_INCOME_PROOF"], axis = 1)

#Count Number of NaNs in FLAG_ACSP_RECORD
sum([x == 'N' for x in data_nans_dropped["FLAG_ACSP_RECORD"]])

#Drop FLAG_ACSP_RECORD
data_nans_dropped = data_nans_dropped.drop(labels = ["FLAG_ACSP_RECORD"], axis = 1)

#Drop Low Age Values (6, 7, 14)
data_nans_dropped["AGE"] = data_nans_dropped["AGE"].replace(6, np.nan)
data_nans_dropped["AGE"] = data_nans_dropped["AGE"].replace(7, np.nan)
data_nans_dropped["AGE"] = data_nans_dropped["AGE"].replace(14, np.nan)
data_nans_dropped = data_nans_dropped.dropna(axis = 0, subset = ["AGE"])

#Drop Product
data_nans_dropped = data_nans_dropped.drop(labels = ["PRODUCT"], axis = 1)

data_clean = pd.DataFrame(data_nans_dropped)
data_clean

"""#4 Modelling

"""

data_clean

"""Since we were thinking about the stability of the model in case of discrimination, we would check that the level of default is more or less the same among all groups:
-Age -Sex -Marital status
"""

df_sex = pd.crosstab(data_clean['SEX'], data_clean['TARGET_LABEL'], normalize='index').mul(100)
df_sex.plot(kind="bar", title="test")
plt.ylabel("Share of default")
plt.xlabel("Sex")

#i'm not sure we know what all these labes mean
data_clean.plot(x="MARITAL_STATUS_1", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="MARITAL_STATUS_2", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="MARITAL_STATUS_3", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="MARITAL_STATUS_4", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="MARITAL_STATUS_5", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="MARITAL_STATUS_6", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="MARITAL_STATUS_7", y="TARGET_LABEL", kind="bar",figsize=(9,8))
plt.show()
plt.ylabel("Share of default")
plt.xlabel("Marital status")

#i'm not sure we know what all these labes mean
data_clean.plot(x="AGE_17_25", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="AGE_26_35", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="AGE_36_45", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="AGE_46_55", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="AGE_56_75", y="TARGET_LABEL", kind="bar",figsize=(9,8))
data_clean.plot(x="AGE_76_PLUS", y="TARGET_LABEL", kind="bar",figsize=(9,8))
plt.show()
plt.ylabel("Share of default")
plt.xlabel("Age")

data_clean.columns

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

X=data_clean[['MONTHS_IN_RESIDENCE', 'TOTAL_INCOME_STD', 'OTHER_INCOMES',
                      'QUANT_CARS', 'COMPANY', 'FLAG_PROFESSIONAL_PHONE', 'PRODUCT_1', 'PRODUCT_2',
        'PRODUCT_7', 'FLAG_CREDIT_CARD']]
y=data_clean[['TARGET_LABEL']]

X.dtypes

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3,random_state=1)

X.isnull().sum()

y.describe()



"""## Logistic Regression

"""

################################Logistic Regression###########################
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import matplotlib.pylab as plt
from dmba import classificationSummary, regressionSummary
from dmba import  gainsChart, liftChart

pip install dmba

c_space = np.logspace(-5, 8, 15)
param_grid = {'C': c_space,'penalty': ['l1', 'l2']}
logreg = LogisticRegression(solver='liblinear')
logreg_cv = GridSearchCV(logreg,param_grid, cv=5)

logreg_cv.fit(X_train,y_train.values.ravel())

print("Tuned Logistic Regression Parameters: {}".format(logreg_cv.best_params_)) 
print("Best score is {}".format(logreg_cv.best_score_))

logreg = LogisticRegression(penalty="l2", C=7.1e-04) ## Changed L1 to L2
logreg.fit(X_train, y_train.values.ravel())

logreg_pred_train=logreg.predict_proba(X_train)

y_train=y_train.values.flatten()

logit_train = pd.DataFrame({'actual': y_train, 
                            'p(0)': [p[0] for p in logreg_pred_train],
                            'p(1)': [p[1] for p in logreg_pred_train],
                            'predicted': logreg.predict(X_train)})



logit_train = logit_train.sort_values(by=['p(1)'], ascending=False)
# confusion matrix
classificationSummary(logit_train.actual, logit_train.predicted)
gainsChart(logit_train.actual, figsize=[5, 5])

logreg_pred_test=logreg.predict_proba(X_test)

y_test=y_test.values.flatten()

logit_test = pd.DataFrame({'actual': y_test, 
                            'p(0)': [p[0] for p in logreg_pred_test],
                            'p(1)': [p[1] for p in logreg_pred_test],
                            'predicted': logreg.predict(X_test)})

logit_test = logit_test.sort_values(by=['p(1)'], ascending=False)
# confusion matrix
classificationSummary(logit_test.actual, logit_test.predicted)
gainsChart(logit_test.actual, figsize=[5, 5])

liftChart(logit_test['p(1)'], title=False)

from sklearn.metrics import classification_report
print(classification_report(y_train,logreg.predict(X_train)))

print(classification_report(y_test,logreg.predict(X_test)))

"""## K-Nearest Neighbor(KNN)"""

######################## Knn KNeighbors ##################################
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
import matplotlib.pylab as plt

param_grid = {'n_neighbors': np.arange(1, 50)}
knn = KNeighborsClassifier()
knn_cv = GridSearchCV(knn, param_grid, cv=5)
knn_cv.fit(X_train, y_train)

cv_scores = cross_val_score(knn_cv, X_train, y_train)
print(cv_scores)

print('Optimal K-nn parameter (number of neighbors): ',knn_cv.best_params_)

knn_cv.best_score_

knn = KNeighborsClassifier(n_neighbors=48)
knn.fit(X_train, y_train)

knnProb_train=knn.predict_proba(X_train)

knn_train = pd.DataFrame({'actual': y_train, 
                            'p(0)': [p[0] for p in knnProb_train],
                            'p(1)': [p[1] for p in knnProb_train],
                            'predicted': knn.predict(X_train)})

knn_train.head(10)

knn_train = knn_train.sort_values(by=['p(1)'], ascending=False)
# confusion matrix
classificationSummary(knn_train.actual, knn_train.predicted)
gainsChart(knn_train.actual, figsize=[5, 5])

liftChart(knn_train['p(1)'], title=False)

knnProb_test=knn.predict_proba(X_test)

knn_test = pd.DataFrame({'actual': y_test, 
                            'p(0)': [p[0] for p in knnProb_test],
                            'p(1)': [p[1] for p in knnProb_test],
                            'predicted': knn.predict(X_test)})

knn_test = knn_test.sort_values(by=['p(1)'], ascending=False)
# confusion matrix
classificationSummary(knn_test.actual, knn_test.predicted)
gainsChart(knn_test.actual, figsize=[5, 5])

liftChart(knn_test['p(1)'], title=False)

print(classification_report(y_train,knn.predict(X_train)))

print(classification_report(y_test,knn.predict(X_test)))



"""## Classification Tree"""

######Classification Tree##################
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
#from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import matplotlib.pylab as plt
from dmba import plotDecisionTree, classificationSummary, regressionSummary

tree = DecisionTreeClassifier()
tree.get_params().keys()

param_dist = {"max_depth": [3, None],
              "min_samples_leaf": np.arange(1, 9),
              "criterion": ["gini", "entropy"]}

tree_cv = GridSearchCV(tree, param_dist, cv=5)

tree_cv.fit(X_train, y_train)

print("Tuned Decision Tree Parameters: {}".format(tree_cv.best_params_))
print("Best score is {}".format(tree_cv.best_score_))

tree = DecisionTreeClassifier(criterion= 'gini',max_depth= 3,min_samples_leaf= 8)

tree.fit(X_train,y_train)

treeProb_train=tree.predict_proba(X_train)

tree_train = pd.DataFrame({'actual': y_train, 
                            'p(0)': [p[0] for p in treeProb_train],
                            'p(1)': [p[1] for p in treeProb_train],
                            'predicted': tree.predict(X_train)})

tree_train = tree_train.sort_values(by=['p(1)'], ascending=False)
# confusion matrix
classificationSummary(tree_train.actual, tree_train.predicted)
gainsChart(tree_train.actual, figsize=[5, 5])

liftChart(tree_train['p(1)'], title=False)

#####A bit better######!!!!!!!!
treeProb_test=tree.predict_proba(X_test)
tree_test = pd.DataFrame({'actual': y_test, 
                            'p(0)': [p[0] for p in treeProb_test],
                            'p(1)': [p[1] for p in treeProb_test],
                            'predicted': tree.predict(X_test)})

tree_test = tree_test.sort_values(by=['p(1)'], ascending=False)
# confusion matrix
classificationSummary(tree_test.actual, tree_test.predicted)
gainsChart(tree_test.actual, figsize=[5, 5])

liftChart(tree_test['p(1)'], title=False)

print(classification_report(y_train,tree.predict(X_train)))

print(classification_report(y_test,tree.predict(X_test)))



"""**Ensemble model**"""

total_valid = pd.DataFrame({'actual': y_test, 
                         'predicted_Logistic': logreg.predict(X_test),
                         'predicted_Knn': knn.predict(X_test),
                        'predicted_Tree': tree.predict(X_test)})

total_valid['Mode']=0

total_valid

mode=total_valid.mode(axis=1)

total_valid['Mode']=mode

total_valid['Mode'].sum()

probability_valid = pd.DataFrame({
                            'LogitRegression: p(1)': [p[1] for p in logreg_pred_test],
                            'KnnRegression: p(1)': [p[1] for p in knnProb_test],
                            'TreeRegression: p(1)': [p[1] for p in treeProb_test]
                         })

mean=probability_valid.mean(axis = 1)

probability_valid['Mean']=mean

list_mean=[]

probability_valid

for x in range(0,14515):
    if probability_valid['Mean'].iloc[x]>=0.3:
        list_mean.append(1)
    else:
        list_mean.append(0)

list_mean= pd.DataFrame(list_mean)

mean_values=list_mean

total_valid['Mean']=mean_values

total_valid

classificationSummary(total_valid.actual, total_valid.Mean)

classificationSummary(total_valid.actual, total_valid.Mode)