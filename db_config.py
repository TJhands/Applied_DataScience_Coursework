from sqlalchemy import create_engine
import setting



ENGINE_PROJECT_ENGLISH = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(setting.MYSQL_USER,
                                                                           setting.MYSQL_PASSWD,
                                                                           setting.MYSQL_HOST_ENGLISH,
                                                                           setting.MYSQL_PORT,
                                                                           'project'),
                              connect_args={'charset': 'utf8'}, pool_size=8)
ENGINE_PROJECT_RUSSIAN = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(setting.MYSQL_USER,
                                                                           setting.MYSQL_PASSWD,
                                                                           setting.MYSQL_HOST_RUSSIAN,
                                                                           setting.MYSQL_PORT,
                                                                           'project'),
                              connect_args={'charset': 'utf8'}, pool_size=8)