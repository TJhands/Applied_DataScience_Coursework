
def get_area_code():
    sql = "select * from areacode"
    return sql
def get_features():
    sql = "select * from features"
    return sql
def get_homelessness():
    sql = "select * from features where feature_name = 'homelessness'"
    return sql