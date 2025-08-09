from tinydb import TinyDB, Query
import time

from datetime import datetime

db = TinyDB("db.json")


class StatusDataMgr:
    def __init__(self):
        self.table = db.table("status_history")
        self.query = Query()

    def __len__(self):
        return len(self.table)

    def create_status(self, status, description):
        now = time.time()
        status_data = {"start_time": now, "end_time": -1, "status": status, "description": description}
        st = datetime.fromtimestamp(now).strftime("%y-%m-%d %H:%M")
        status_data["start_time_str"] = st
        status_data["end_time_str"] = "现在"
        status_data["index"] = self.get_max_index() + 1
        return status_data

    def append_status(self, status: dict):
        now = status["start_time"] - 1
        self.touch_status(now)
        self.table.insert(status)

    def get_max_index(self):
        docs = self.table.all()
        mx = 0
        for doc in docs:
            mx = max(mx, doc["index"])
        return mx

    def touch_status(self, timestamp):
        if len(self.table.all()) > 0:
            last = self.table.get(self.query.index == self.get_max_index())
            last["end_time"] = timestamp
            st = datetime.fromtimestamp(timestamp).strftime("%y-%m-%d %H:%M")
            last["end_time_str"] = st
            self.table.update(last, self.query.index == self.get_max_index())

    def get_present_status(self):
        return self.table.get(self.query.index == self.get_max_index())

    def get_history_status(self):
        docs = self.table.search(self.query.index < self.get_max_index())
        sorted_docs = sorted(docs, key=lambda doc: doc["index"], reverse=True)
        return sorted_docs

    def remove_old_status(self):
        if len(self.table.all()) > 80:  # 最大长度,可以更新成可配置的值
           self.table.remove(self.query.index < self.get_max_index()-80)