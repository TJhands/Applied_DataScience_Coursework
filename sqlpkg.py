
sql_test = "SELECT postID,flatContent FROM exetools_post LIMIT 1"
sql_postdate = "SELECT postDate,flatContent FROM exetools_post where authorName != '' and authorName is not NULL "
sql_user_time = "SELECT postID,authorName,postDate FROM exetools_post WHERE authorName != '' and authorName is not NULL "
def get_data(table):
    sql = "SELECT authorName,postDate,flatContent FROM {} where authorName != '' and authorName is not NULL and flatContent != '' and flatContent is not NULL order by authorName,postDate".format(table)
    return sql
