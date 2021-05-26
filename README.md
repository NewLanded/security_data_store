# security_data_store
store stock data get from tushare

linux depended:
    gcc
    python-devel
    mysql-devel

pip install:
    schedule  # apache-airflow 1.10有bug, 暂时用schedule,  apache-airflow  # export SLUGIFY_USES_TEXT_UNIDECODE=yes
    pandas
    bs4
    tushare
    # mysql-connector  # 速度不如mysqlclient, 但依赖少, 安装简单, 好像换成 pip install PyMySQL  这个了
    # mysqlclient  # mysqlclient  # sudo ln -s /usr/lib64/libmariadbclient.a /usr/lib64/libmariadb.a  # https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
    xlrd
    psycopg2-binary
    asyncpg




设置环境变量:SLUGIFY_USES_TEXT_UNIDECODE=yes
设置动态库连接(是个bug, 以后的版本可能会修复): sudo ln -s /usr/lib64/libmariadbclient.a /usr/lib64/libmariadb.a
sqlalchemy连接字符串: DB_CONNECT = 'mysql+mysqlconnector://root:password@localhost:3306/test?charset=utf8'

mysql配置:
show variables like 'explicit_defaults_for_timestamp'; 
[mysqld]
explicit_defaults_for_timestamp=true


错误处理:
1. MySQL Connection not available
   原因是sqlalchemy的session过期, 详见 https://mofanim.wordpress.com/2013/01/02/sqlalchemy-mysql-has-gone-away/
                                       https://blog.csdn.net/u013673976/article/details/45939297
   show global variables like '%timeout%';  # 查看mysql连接过期时间
   解决: sqlalchemy创建连接时加参数 pool_recycle=3600


nohup /home/stock/anaconda3/envs/stock/bin/python /home/stock/app/security_data_store/timed_task.py > /dev/null 2>&1 &

