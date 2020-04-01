开发环境
1 ）本地，测试，生产环境
from manufacture.deploy.dev import *
# from manufacture.deploy.dev import *
# from manufacture.deploy.uat import *

2 ）测试云，正是云部署
1 下载代码，运行docker-compose down , docker-compose up -d
注意：测试云使用dev分支， 正是云使用 master 分支

3 开发规范
1）gitflow
https://www.jianshu.com/p/cb96825ff89e
2）pull-request
https://www.cnblogs.com/selimsong/p/9059964.html

4 创建superuser
docker exec -it 容器名 python manage.py createsuperuser
