# 雪球网爬虫

抓取大V的粉丝，然后一对一发送消息

### 安装:

需要Python环境，推荐[virtualenv](https://virtualenv.pypa.io/en/latest/userguide.html#usage)

需要[Sqlite](http://www.runoob.com/sqlite/sqlite-installation.html)

进入项目根目录

        pip install -r req.txt


配置

        cp config.sample.py config.py

config需要配置用户名，密码和要发送的消息


### 启动运行环境

进入工作目录，然后执行(通常来说，env放在了跟工作目录平级，这里命名成了spider-env)

        source ../spider-env/bin/activate

### 执行：

        python main.py [to_do]

比如抓取粉丝

        python main.py crawl_people_info

可以执行的操作

| 操作              | 解释           |
|------------------|----------------|
|crawl_people_info | 抓取粉丝        |
|send_chat_msg     | 发送消息        |
|post              | 发帖子          |
|remove_chat_history  | 删除发送历史，执行后，发送消息会从头开始 |
|remove_post_history  | 删除发送广播历史，执行后，发送广播会从头开始 |
|remove_login      | 登出           |
|remove_all_people | 删除数据库中保存的所有粉丝信息 |
|clear_log         | 清除日志        |
