# Applied_DataScience_Coursework

## **`Data`**:  
>https://www.gov.uk/government/statistical-data-sets/live-tables-on-house-building
>>permanent dwellings started and completed by three tenures:("PrivateEnterprise","Housing Associations","LocalAuthority"
) 2005Q1-2019Q4 quarter

>https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness
>>homelessness_england   2017Q1-2019Q3 quarter

>https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-january-2020?utm_medium=GOV.UK&ut
 >>sales_volume: 1998-2019 all annual and all quarter  
 house_price_index: 1998-2019 all annual and all quarter  
 
 >https://www.gov.uk/government/statistical-data-sets/live-tables-on-affordable-housing-supply
>>Total affordable dwelling supply 2005-2018 annual

>https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationprojections/datasets/householdprojectionsforenglanddetaileddataformodellingandanalysis
>>households projection 2011-2019 annual for normalisation

 >https://www.gov.uk/government/statistics/help-to-buy-equity-loan-scheme-statistics-april-2013-to-30-september-2019-england
>>help to buy 2014(Q1)-2019(Q3) all quarter England; it shows the complete number of sales of help to buy for the first-time buyer, by the local authority. 
The normalization part: Used the number of sales of help to buy divided the number of local households.

 >https://www.nomisweb.co.uk/query/asv2htm.aspx
>>unemployment rate 2016-2019 annual England Scotland Wales

>>weekly pay change (%) for different group(median)

>>```
>>variables
>>1 unemployment
>>2 male_full_time
>>3 male_part_time
>>4 female_full_time
>>5 female_part_time
>>6 full_time
>>7 part_time
>>```

## total features:
```
0 homelessness   normalised and /max
1 Households_with_one_dependent_child
2 Households_with_three_or_more_dependent_children
3 Households_with_two_dependent_children
4 One_person_households__Female
5 One_person_households__Male
6 Other_households_with_two_or_more_adults
7 Male
8 Female
9 age_under29
10 unemployment
11 male_full_time
12 male_part_time
13 female_full_time
14 female_part_time
15 full_time
16 part_time
17 help_to_buy  normalised and /max
18 hpi  normalised and /max
19 sales volume  normalised and /max
20 new dwelling start  normalised and /max
21 new dwelling complete  normalised and /max
PS:  
feature 0 is the number of households assessed as homeless
features 1-6 are percentages of household type
features 7-9 are based on the age and gender of the household reference person, (percentage of) 
feature 10 is unemployment rate
features 11- 16 are weekly pay change(%) based on different type of work and different gender
feature 17 is sales volumes of dwellings through "help to buy"
feature 18 house price index
feature 19 total sales volumes of dwellings
feature 20 and 21 the number of dwellings started and completed
```



 draw_multi可以回归
 改变和添加X:
#y=homelessness
#x=sales_volume+hpi
fit = smf.ols('homelessness~sales_volume+hpi', data = Train).fit()
