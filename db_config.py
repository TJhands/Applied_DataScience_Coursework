from sqlalchemy import create_engine
import setting



ENGINE_ADS_COURSEWORK = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(setting.MYSQL_USER,
                                                                           setting.MYSQL_PASSWD,
                                                                           setting.MYSQL_HOST_ENGLISH,
                                                                           setting.MYSQL_PORT,
                                                                           'ads_coursework'),
                              connect_args={'charset': 'utf8'}, pool_size=8)