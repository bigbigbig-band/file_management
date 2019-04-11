# -*- code:utf-8 -*-
import os
import shutil
import threading
import socket
import sys
import json


class StaticFileServer(object):
    def __init__(self, port):
        # 初始化套接字
        self.__socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.__socket_server.bind(("", port))
        self.__socket_server.listen(128)
        self.json_data = None

    # 等待客户端线程函数
    def wait_client_threading(self, socket_server):
        # 当有客户端连接时，建立一个新的线程用于处理客户端的请求
        while True:
            socket_client, address = socket_server.accept()
            print(f"客户端{address}已连接！")
            client_threading = threading.Thread(target=self.handle_client_request, args=(socket_client, address))
            client_threading.setDaemon(True)
            client_threading.start()

    def handle_client_request(self, client_socket, address):
        # 处理客户端请求函数
        client_address = address
        while True:
            request = client_socket.recv(1024*1024*5)
            if not request:
                # 请求为空,退出线程
                print(f"客户端{client_address}已下线")
                break
            # 分割请求
            print(request)
            request = request.decode("utf-8")
            request_split_list = request.split(" ", 2)
            # 判断请求路径是否为空，为空则返回首页
            if "GET" in request_split_list[0]:
                response = self.handle_get(request_split_list[1])
                client_socket.send(response)
                client_socket.close()
                break
            else:
                # 获得post请求体
                post_request_body = self.get_post_request_body(request)
                # 解析json为字典
                post_request_body_dic = json.loads(post_request_body)
                # 处理post请求，并返回响应体
                response = self.handle_post(post_request_body_dic)
                client_socket.send(response)
                client_socket.close()
                break

    # 获得请求体
    @staticmethod
    def get_post_request_body(request):
        post_body = request.split("\r\n\r\n", 2)[1]
        return post_body

    # 处理post请求
    def handle_post(self, request_body_dic):
        # 删除文件或者文件夹
        if request_body_dic["command"] == "del":
            del_false_list = []
            for item in request_body_dic["path"]:
                if os.path.isdir(item):
                    try:
                        # 递归删除文件
                        shutil.rmtree(item)
                    except PermissionError:
                        del_false_list.append(item)
                    # 确认文件是否删除
                    else:
                        if os.path.exists(item):
                            del_false_list.append(item)
                else:
                    try:
                        # 递归删除文件
                        os.remove(item)
                    except PermissionError:
                        del_false_list.append(item)
                    # 确认文件是否删除
                    else:
                        if os.path.exists(item):
                            del_false_list.append(item)
            response_body = json.dumps({"delfalse": del_false_list})

        # 移动文件
        elif request_body_dic["command"] == "move":
            move_false_list = []
            for i in range(1, len(request_body_dic["path"])):
                try:
                    # 移动文件文件
                    shutil.move(request_body_dic["path"][0]+"/"+request_body_dic["path"][i], request_body_dic["2path"])
                except Exception and PermissionError:
                    move_false_list.append(request_body_dic["path"][i])
                # 确认文件是否移动
                else:
                    if os.path.exists(request_body_dic["path"][i]):
                        move_false_list.append(request_body_dic["path"][i])
            response_body = json.dumps({"movefalse": move_false_list})

        # 新建文件夹
        elif request_body_dic["command"] == "new_dir":
            dir_path = request_body_dic["path"][0]+"/"+request_body_dic["path"][1]
            if os.path.exists(dir_path):
                response_body = json.dumps({"new_dir_false": -1})
            else:
                try:
                    os.mkdir(dir_path)
                except PermissionError:
                    response_body = json.dumps({"new_dir_false": -2})
                else:
                    response_body = json.dumps(["new_dir_true"])

        elif request_body_dic["command"] == "uploading":
            str1 = request_body_dic["file_bin"]
            print(str1)
            # for code in request_body_dic["file_bin"]:
            #     str_bin += hex(int(code))
            # file = os.open(request_body_dic["file_info"]["path_this"]+"/"+request_body_dic["file_info"]["file_name"], os.O_WRONLY|os.O_CREAT)


        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        # 响应头
        response_head = "BWS/1.1\r\n"
        response = response_line+response_head+"\r\n"+response_body
        return response.encode("utf-8")

    # 处理GET请求
    def handle_get(self, request_body):
        if len(request_body) == 1:
            response = self.get_file_response("html/index.html")
        elif "icon" in request_body:
            # 响应浏览器请求图标
            response = self.get_file_response("img/icon_file.png")
        elif "/?" in request_body:
            if "pathfile" in request_body:
                path_this = (request_body.split(","))[1]
                disk_size = self.get_disk_size(path_this)
                response = self.get_path_response(disk_size, path_this)
            # 请求路径是否为目录
            elif os.path.isdir(request_body[2:]):
                path_this = request_body[2:]
                disk_size = self.get_disk_size(path_this)
                response = self.get_path_response(disk_size, path_this)
            else:
                path_this = request_body[2:]
                response = self.get_file_response(path_this)
        else:
            response = self.get_file_response(request_body[1:])
        return response

    # 获得路径请求的响应体
    def get_path_response(self, size, path):
        if os.path.isdir(path):
            list_path = self.get_path(path)
            # 末尾加一个/,方便后面FOR循环判断是否为文件夹
            if path != "/":
                path += "/"
            if list_path != -1:
                list_isdir = self.get_isdir_list(path, list_path)
            else:
                list_isdir = []
            response_body = {"size": size, "list_path": list_path, "list_isdir": list_isdir}
            response_line = "HTTP/1.1 200 OK\r\n"
            # 响应头
            response_head = "BWS/1.1\r\n"
        else:
            response_body = {"size": size, "list_path": -1, "list_isdir": -1}
            response_line = "HTTP/1.1 200 OK\r\n"
            # 响应头
            response_head = "BWS/1.1\r\n"
        return (response_line+response_head+"\r\n"+json.dumps(response_body)).encode("utf-8")

    # 判断是否为文件夹
    @staticmethod
    def get_isdir_list(path_this, list_path):

        list_isdir = []
        for item in list_path:
            if os.path.isdir(path_this + item):
                list_isdir.append("Dir")
            else:
                if "." in item:
                    index = item.rindex(".")
                    list_isdir.append(item[index + 1:])
                else:
                    list_isdir.append(" ")
        return list_isdir

    # 获得该路径下的所有文件
    @staticmethod
    def get_path(path):
        try:
            dir_list = os.listdir(path)
        except PermissionError:
            return -1
        else:
            return dir_list

    # 获得磁盘容量
    @staticmethod
    def get_disk_size(path):
        size_all = int(os.statvfs(path).f_blocks * os.statvfs(path).f_bsize / 10 ** 8)
        size_free = int((os.statvfs(path).f_bsize * os.statvfs(path).f_bfree) / 10 ** 8)
        return [size_all/10, size_free/10]

    # 获得文件列表
    @staticmethod
    def get_file_response(path):
        try:
            with open(path, "rb") as file:
                file_data = file.read()

        except Exception as e:
            # 响应行
            response_line = "HTTP/1.1 404 Not Found\r\n"
            # 响应头
            response_head = "BWS/1.1\r\n"
            return (response_line + response_head + "\r\n").encode("utf-8")

        else:
            # 响应行
            response_line = "HTTP/1.1 200 OK\r\n"
            # 响应头
            response_head = "BWS/1.1\r\n"
            return (response_line + response_head + "\r\n").encode("utf-8") + file_data

    # 服务器启动
    def start_server(self):
        wait_client_threading = threading.Thread(target=self.wait_client_threading, args=(self.__socket_server,))
        wait_client_threading.setDaemon(True)
        wait_client_threading.start()


def main():
    port = sys.argv[1]
    if port.isdigit():
        server = StaticFileServer(int(port))
        server.start_server()
    while True:
        key = input("请输入0退出服务器！")
        if key == "0":
            break


if __name__ == "__main__":
    main()
