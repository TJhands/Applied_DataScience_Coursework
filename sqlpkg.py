
def get_area_code():
    sql = "select * from areacode"
    return sql
def get_features():
    sql = "select `area_code`,`year`,`quarter`,`feature_name`,`feature_value` from features where area_code != '-' and area_code != 'E92000001' and area_code like 'E%%' and `year`>= 2011"
    return sql
def get_features_nomalised():
    sql = "select `area_code`,`year`,`quarter`,`feature_name`,`feature_value_normalised` as `feature_value` from features where area_code != '-' and area_code != 'E92000001' and area_code like 'E%%' and `year`>= 2011 and `quarter` = 'Q1'"
    return sql
def get_homelessness():
    sql = "select `area_code`,`year`,`quarter`,`feature_name`,`feature_value`,`feature_value_normalised` from features where feature_name = 'homelessness'and area_code like 'E%%' and `year`>= 2011"
    return sql
def get_area_code_england():
    sql = "select * from areacode where area_code like 'E%%'"
    return sql
def get_area_code_scotland():
    sql = "select * from areacode where area_code like 'S%%'"
    return sql
def get_features_except_hpi():
    sql = "select `area_code`,`year`,`quarter`,`feature_name`,`feature_value` from features where area_code like 'E%%' and feature_name != 'hpi' and `year`>= 2011"
    return sql
def get_total_households():
    sql = "select `area_code`,`year`,`value` from households where area_code like 'E%%' and age_group = 'all'"
    return sql
def get_features_hpi():
    sql = "select `area_code`,`year`,`quarter`,`feature_name`,`feature_value` from features where area_code like 'E%%' and feature_name = 'hpi' and `year`>= 2011"
    return sql
def get_features_help_to_buy():
    sql = "select `area_code`,`year`,`quarter`,`feature_name`,`feature_value` from features where area_code like 'E%%' and feature_name = 'help_to_buy' and `year`>= 2011"
    return sql
def get_household_by_househould_type():
    sql = "select `area_code`,`year`,`category_value`,`value` from households where area_code like 'E%%' and category_name = 'household_type'"
    return sql
def get_household_by_all():
    sql = "select `area_code`,`year`,`value` from households where area_code like 'E%%' and age_group = 'all'"
    return sql
def get_household_by_sex():
    sql = "select `area_code`,`year`,`category_value`,`value` from households where area_code like 'E%%' and category_name = 'sex'"
    return sql
def get_household_by_age():
    sql = "select `area_code`,`year`,`value` from households where area_code like 'E%%' and category_name = 'sex' and (age_group = '16-19' or age_group = '20-24' or age_group = '25-29')"
    return sql
def get_features_nomalised_scotland():
    sql = "select `area_code`,`year`,`quarter`,`feature_name`,`feature_value_normalised` as `feature_value` from features where area_code like 'S%%'"
    return sql