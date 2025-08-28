from tinydb import TinyDB, Query
import time

from datetime import datetime

db = TinyDB("db.json")

backup_db=TinyDB("backup.json")


class StatusDataMgr:
    def __init__(self):
        self.status_table = db.table("status_history")
        self.backup_table = backup_db.table("status_history")
        self.max_status_num=80 # 保存状态的最大长度
        self.query = Query()

    def __len__(self):
        return len(self.status_table)

    def create_status(self, status, description):
        """
        生成一个状态字典,包括状态和状态描述

        时间会根据服务器时间自动插入字典
        :param status: 状态名
        :param description: 描述内容
        :return:
        """
        now = time.time()
        status_data = {"start_time": now, "end_time": -1, "status": status, "description": description}
        st = datetime.fromtimestamp(now).strftime("%y-%m-%d %H:%M")
        status_data["start_time_str"] = st
        status_data["end_time_str"] = "现在"
        status_data["index"] = self.get_max_index() + 1
        return status_data

    def append_status(self, status: dict):
        """
        插入一个最新状态字典
        :param status: 要插入的状态字典
        :return:
        """
        now = status["start_time"] - 1
        self.touch_status(now)
        self.status_table.insert(status)

    def get_max_index(self):
        """
        遍历全表找到最新的索引值
        :return:
        """
        docs = self.status_table.all()
        mx = 0
        for doc in docs:
            mx = max(mx, doc["index"])
        return mx

    def touch_status(self, timestamp):
        """
        设置上一个状态的结束时间为当前时间
        :param timestamp: 当前时间戳
        :return:
        """
        if len(self.status_table.all()) > 0:
            last = self.status_table.get(self.query.index == self.get_max_index())
            last["end_time"] = timestamp
            st = datetime.fromtimestamp(timestamp).strftime("%y-%m-%d %H:%M")
            last["end_time_str"] = st
            self.status_table.update(last, self.query.index == self.get_max_index())
            # 当前结束的状态会加入备份文件当中
            last = self.status_table.get(self.query.index == self.get_max_index())
            self.backup_table.insert(last)


    def get_present_status(self):
        """
        获取当前状态对应的状态字典
        """
        return self.status_table.get(self.query.index == self.get_max_index())

    def get_history_status(self):
        """
        获取除当前状态以外的其他状态字典
        :return:
        """
        docs = self.status_table.search(self.query.index < self.get_max_index())
        sorted_docs = sorted(docs, key=lambda doc: doc["index"], reverse=True)
        return sorted_docs

    def remove_old_status(self):
        """
        删除超过长度的状态字典,来保证页面只渲染有限的内容
        ...其实应该用动态加载,但是我暂时并不会写
        :return:
        """
        if len(self.status_table.all()) > self.max_status_num:
           self.status_table.remove(self.query.index < self.get_max_index() - 80)

class PostDataMgr:
    def __init__(self):
        self.post_table = db.table("post_history")
        self.backup_table = backup_db.table("post_history")
        self.query = Query()

    def __len__(self):
        return len(self.post_table)

    def create_post(self, post_content:str, post_tag:str):
        """
        创建一个感想字典
        :param post_content: 感想内容,可能为多行文本
        :param post_tag: 感想标签,为简短介绍
        :return:包含时间,内容和标签的感想字典(dict)
        """
        now = time.time()
        post_data = {"time": now, "post_content": post_content, "post_tag": post_tag}
        st = datetime.fromtimestamp(now).strftime("%y-%m-%d %H:%M")
        post_data["time_str"] = st
        post_data["index"] = self.get_max_index() + 1
        return post_data

    def get_max_index(self):
        """
        遍历全表找到最新的索引值
        :return:
        """
        docs = self.post_table.all()
        mx = 0
        for doc in docs:
            mx = max(mx, doc["index"])
        return mx

    def append_post(self, post: dict):
        """
        插入一个最新感想字典
        :param post: 要插入的感想字典
        :return:
        """
        self.backup_table.insert(post)
        self.post_table.insert(post)

    def get_all_post(self):
        return self.post_table.all()

class SignDataMgr:
    def __init__(self):
        self.sign_table = db.table("sign_history")
        self.backup_table = backup_db.table("sign_history")
        self.query = Query()

    def __len__(self):
        return len(self.sign_table)

    def update_sign(self, sign_content:str):
        post_data = {"time": time.time(), "content": sign_content,"index": self.get_max_index()+1}
        self.sign_table.insert(post_data)
        self.backup_table.insert(post_data)

    def get_max_index(self):
        """
        遍历全表找到最新的索引值
        :return:
        """
        docs = self.sign_table.all()
        mx = 0
        for doc in docs:
            mx = max(mx, doc["index"])
        return mx

    def get_present_sign(self):
        """
        获取当前状态对应的状态字典
        """
        return self.sign_table.get(self.query.index == self.get_max_index())


