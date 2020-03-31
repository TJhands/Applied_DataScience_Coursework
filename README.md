# Applied_DataScience_Coursework

**`Data`**:  
>https://www.gov.uk/government/statistical-data-sets/live-tables-on-house-building
>>permanent dwellings started and completed by three tenures:("PrivateEnterprise","Housing Associations","LocalAuthority"
)

>https://www.gov.uk/government/statistical-data-sets/live-tables-on-homelessness
>>homelessness_england   

>https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-january-2020?utm_medium=GOV.UK&ut
 >>sales_volume: 1998-2019 all annual and all quarter  
 house_price_index: 1998-2019 all annual and all quarter  
 
 draw_multi可以回归
 改变和添加X:
#y=homelessness
#x=sales_volume+hpi
fit = smf.ols('homelessness~sales_volume+hpi', data = Train).fit()
