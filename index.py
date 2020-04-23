#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
 
import redis
from flask import Flask
app = Flask(__name__)


"""

CREATE TABLE IF NOT EXISTS `events`(
   `id` INT UNSIGNED AUTO_INCREMENT , 
   `user_id` VARCHAR(100) NOT NULL COMMENT "用户id",
   `from_id` VARCHAR(100) NOT NULL COMMENT "源id",
   `target_id` VARCHAR(100) NOT NULL COMMENT "目标id",
   `action` VARCHAR(100) NOT NULL COMMENT "对目标的操作，比如创建仓库，关注某人，fork项目",
   `created_at` datetime,
   PRIMARY KEY ( `user_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT "事件表";


CREATE TABLE IF NOT EXISTS `user`(
   `id` INT UNSIGNED AUTO_INCREMENT , 
   `user_name` VARCHAR(100) NOT NULL COMMENT "用户名",
   `created_at` datetime,
   PRIMARY KEY ( `user_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT "用户表";


CREATE TABLE IF NOT EXISTS `user`(
   `id` INT UNSIGNED AUTO_INCREMENT , 
   `user_name` VARCHAR(100) NOT NULL COMMENT "用户名",
   `created_at` datetime,
   PRIMARY KEY ( `user_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT "用户表";

"""


"""
使用推技术，把消息推给粉丝的timelines里面
"""

def msg_produce():
    redis_ins = redis()
    # 使用Redis incr生成唯一的msgID
    msg_id = redis_ins.incr("global:msgID")

    user_id = 1
    msg_data = {
        "user_id": user_id,
        "timestamp": "1587601324",
        "action": "关注",
        "target_info": {
            "url": "xx.xx",
            "name": "xx",
            "user": ""
        },
        "from_info": {
            "url": "xx.xx",
            "name": "xx"
        } 
    }

    msg_data = json.dumps(msg_data)
    redis_ins.set(msg_id, msg_data)

    # 获取自己的粉丝列表, 并把消息写入他们的时间线
    follower_ids = redis_ins.smember("{user_id}:followers".format(user_id))
    for follower_id in follower_ids:
        redis_ins.lpush("{follower_id}:timeline".format(follower_id), msg_id)



@app.route('/')
def get_timelines(page, limit):
    start = (page-1) * limit
    redis_ins = redis()
    user_id = 2
    msg_ids = redis_ins.lrange("{user_id}:timeline".format(user_id), start, end+limit)
    result = []
    for msg_id in msg_ids:
        data = json.loads(redis.get(msg_id))
        result.append(data)

    return result

