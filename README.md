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

 >https://www.nomisweb.co.uk/query/asv2htm.aspx
>>unemployment rate 2016-2019 annual England Scotland Wales 

>>weekly pay change (%) for different group
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

## new features:
```
1 Households_with_one_dependent_child
2 Households_with_three_or_more_dependent_children
3 Households_with_two_dependent_children
4 One_person_households__Female
5 One_person_households__Male
6 Other_households_with_two_or_more_adults
7 Male
8 Female
9 age_under29
```



 draw_multi可以回归
 改变和添加X:
#y=homelessness
#x=sales_volume+hpi
fit = smf.ols('homelessness~sales_volume+hpi', data = Train).fit()
