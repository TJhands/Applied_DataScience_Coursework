
def get_data(table):
    sql = "SELECT authorName,postDate,flatContent FROM {} where authorName != '' and authorName is not NULL and flatContent != '' and flatContent is not NULL order by authorName,postDate".format(table)
    return sql
