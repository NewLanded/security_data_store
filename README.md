# security_data_store
store stock data get from tushare

linux depended:
    gcc
    python-devel
    mysql-devel

pip install:
    apache-airflow  # export SLUGIFY_USES_TEXT_UNIDECODE=yes
    pandas
    bs4
    tushare
    mysql-connector
    # mysqlclient  # mysqlclient  # sudo ln -s /usr/lib64/libmariadbclient.a /usr/lib64/libmariadb.a
    xlrd




设置环境变量:SLUGIFY_USES_TEXT_UNIDECODE=yes
设置动态库连接(是个bug, 以后的版本可能会修复): sudo ln -s /usr/lib64/libmariadbclient.a /usr/lib64/libmariadb.a
sqlalchemy连接字符串: DB_CONNECT = 'mysql+mysqlconnector://root:password@localhost:3306/test?charset=utf8'

mysql配置:
show variables like 'explicit_defaults_for_timestamp'; 
[mysqld]
explicit_defaults_for_timestamp=true
    



定时任务地址: http://47.92.6.148:6676/admin/
