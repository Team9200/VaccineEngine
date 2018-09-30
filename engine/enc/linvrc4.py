# -*- coding:utf-8 -*-
# Author : kjy
# Date : 18. 9. 27
# Version : v1.0
# Explanation : RC4 암/복호화

class RC4:
    # function : __init__(self)
    # Explanation : 변수 초기화
    def __init__(self):
        self.__S = list()
        self.__T = list()
        self.__Key = list()
        self.__K_i = 0
        self.__K_j = 0

    # function : set_key(self, password)
    # Explanation : 키설정
    # input : password - 암호문
    def set_key(self, password):
        for i in range(len(password)):
            self.__Key.append(ord(password[i]))
        self.__init_rc4()

    # function : crypt(self, data)
    # Explanation : 데이터 암/복호화
    # input : data - 암/복호화 할 데이터
    # return : ret_s - 암/복호화 된 데이터
    def crypt(self, data):
        t_str = list()

        for i in range(len(data)):
            t_str.append(ord(data[i]))

        for i in range(len(t_str)):
            t_str[i] ^= self.__gen_k()

        ret_s = ''
        for i in range(len(t_str)):
            ret_s += chr(t_str[i])
        
        return ret_s

    # function : __init_rc4(self)
    # Explanation : RC4 테이블 초기화
    def __init_rc4(self):
        for i in range(256):
            self.__S.append(i)
            self.__T.append(self.__Key[i % len(self.__Key)])

        j = 0
        for i in range(256):
            j = (j + self.__S[i] +  self.__T[i]) % 256
            self.__swap(i, j)

    # function : __swap(self, i, j)
    # Explanation : i j 값 교환
    # input : i, j - 교환할 값
    def __swap(self, i, j):
        temp = self.__S[i]
        self.__S[i] = self.__S[j]
        self.__S[j] = temp

    # function : __gen_k(self)
    # Explanation : 암/복호화에 필요한 스트림 생성
    # return : self.__S[t] - 암/복호화에 필요한 스트림
    def __gen_k(self):
        i = self.__K_i
        j = self.__K_j

        i = (i + 1) % 256
        j = (j + self.__S[i]) % 256
        self.__swap(i, j)
        t = (self.__S[i] + self.__S[j]) % 256

        self.__K_i = i
        self.__K_j = j

        return self.__S[t]
