#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
 
import redis
from flask import Flask
app = Flask(__name__)



"""
思路：
使用推技术，每个用户或仓库有变动的时候把消息推给粉丝的timelines里面

生产消息：
    1. 使用redis incr给每个消息生成唯一的msgID
    2. 变动的事件包括关注，fork，创建仓库，以及user_id, 变动对象的信息都写入到一个字典里面，然后序列化后存到redis的msgId里面
    3. 获取当前用户的粉丝列表，数据结构是set，用smember获取粉丝id
    4. 每个粉丝都维护一个timeline队列，遍历粉丝列表，给他们的timeline队列添加msgID

获取消息：
    1. 每个粉丝上来就获取自己的timeline队列


"""

def msg_produce():
    redis_ins = redis()
    # 使用Redis incr生成唯一的msgID
    msg_id = redis_ins.incr("global:msgID")

    # 消息内容
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

    # redis存储消息，msg_id->msg_data
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
    # 根据页数和limit逐页获取
    msg_ids = redis_ins.lrange("{user_id}:timeline".format(user_id), start, end+limit)
    result = []
    for msg_id in msg_ids:
        data = json.loads(redis.get(msg_id))
        result.append(data)

    return result

