#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import numpy as np
from networkx.classes.function import all_neighbors

class Metrics:
    def __init__(self,users,R,id_list,g):
        # 用户数据
        self.users = users
        # 用户总个数
        self.num = len(users)
        # 代表性矩阵
        self.R = R
        # 在图中对应的节点编号
        # 转换成字典
        self.id_dic = dict(zip(id_list,range(len(id_list))))
        # 关系图
        self.g = g
        # id_list
        self.id_list = id_list


    # 根据pandas里的索引返回对应的userid
    def GetID(self,profiles):
        return list(self.users.loc[profiles]['userid'])

    # 获得用户的邻居
    def GetNeighbours(self,u):
        if self.id_dic[str(u)] in self.g:
            return set([int(self.id_list[i]) for i in all_neighbors(self.g,self.id_dic[str(u)])])
        else:
            return set()

    # 计算特征代表性
    def Rc(self,users,profiles,R):
        '''

        :param users: DataFrame类型
        :param profiles: 代表性候选集
        :param R: 代表性矩阵
        :return: 返回代表性值
        '''
        # 找到profiles对应的index
        rows = [users[(users['userid'] == u)].index[0] for u in profiles]
        # R中找rows中每列最大值
        # return np.sum(np.max(R[rows,:],axis=0),axis=0) / self.num
        # R中找rows中的每列平均值
        return np.sum(np.mean(R[rows,:],axis=0),axis=0) / self.num

    # 计算结构代表性
    def Rt(self,profiles):
        neighbours = reduce(lambda x,y:x | y,[set(all_neighbors(self.g,self.id_dic[str(u)])) if self.id_dic[str(u)] in self.g else set() for u in profiles])
        NS = len(neighbours - set(profiles))
        VS = self.num - len(profiles)
        return 1.0 * NS / VS

    # 目标函数
    def RScore(self,profiles):
        rc = self.Rc(self.users,profiles,self.R)
        rt = self.Rt(profiles)
        return rc,rt,2.0 * rc * rt / (rc + rt)
