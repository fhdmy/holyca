import os
from paramiko import SSHClient, AutoAddPolicy, AuthenticationException,Transport,SFTPClient
import sys

class Update:
    host="101.133.226.16"
    port=22
    username='root'
    password="Jch199669"
    project_url="/Users/jiang/HolyCA"
    nginx_url="/usr/share/nginx"
    _ssh=None

    def handle_files(self):
        # web
        try:
            os.chdir(f"{self.project_url}/web/caweb")
            os.system("yarn build")
            os.system("zip -r html.zip dist")
        except Exception as e:
            raise ConnectionError('zip web packages error: %s' % e)
        # server
        try:
            os.chdir(f"{self.project_url}/server")
            os.system(f"{self.project_url}/server/datavis/bin/pip freeze>{self.project_url}/server/caserver/requirements.txt")
            os.system("zip -r caserver.zip caserver")
        except Exception as e:
            raise ConnectionError('zip server packages error: %s' % e)
        print("zip files finished!")

    def transport(self):
        transport = Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = SFTPClient.from_transport(transport)
        sftp.put(f'{self.project_url}/web/caweb/html.zip', f'{self.nginx_url}/html.zip')
        sftp.put(f'{self.project_url}/server/caserver.zip', f'{self.nginx_url}/server/new_caserver.zip')
        print("transport finished!")
        transport.close()

    def operate_remote(self,exchange_db):
        self._ssh = SSHClient()
        self._ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self._ssh.connect(self.host, username=self.username, password=self.password, port=self.port)
            print("ssh connect success!")
            self._ssh.exec_command(f"unzip -o {self.nginx_url}/html.zip -d {self.nginx_url}")
            self._ssh.exec_command(f"cp -frap {self.nginx_url}/dist/* {self.nginx_url}/html/")
            # self._ssh.exec_command(f"rm -rf {self.nginx_url}/dist")

            self._ssh.exec_command(f"mkdir {self.nginx_url}/server/new_caserver")
            self._ssh.exec_command(f"unzip -o {self.nginx_url}/server/new_caserver.zip -d {self.nginx_url}/server/new_caserver")
            
            # self._ssh.exec_command(f"rm -r {self.nginx_url}/html.zip ")
            # self._ssh.exec_command(f"rm -r {self.nginx_url}/server/new_caserver.zip ")
            self._ssh.exec_command(f"rm -r {self.nginx_url}/server/new_caserver/caserver/manage.log")
            if exchange_db:
                self._ssh.exec_command(f"cp -frap {self.nginx_url}/server/new_caserver/caserver/* {self.nginx_url}/server/caserver/")
            else:
                try:
                    self._ssh.exec_command(f"rm -r {self.nginx_url}/server/new_caserver/caserver/db.sqlite3")
                    self._ssh.exec_command(f"cp -frap {self.nginx_url}/server/new_caserver/caserver/* {self.nginx_url}/server/caserver/")
                    self._ssh.exec_command(f"{self.nginx_url}/server/datavis/bin/pip install -r {self.nginx_url}/server/caserver/requirements.txt")
                    self._ssh.exec_command(f"{self.nginx_url}/server/datavis/bin/python3 {self.nginx_url}/server/caserver/manage.py makemigrations")
                    self._ssh.exec_command(f"{self.nginx_url}/server/datavis/bin/python3 {self.nginx_url}/server/caserver/manage.py migrate")
                    # self._ssh.exec_command(f"rm -rf {self.nginx_url}/server/new_caserver/caserver")
                except Exception as e:
                    raise ConnectionError('remote cmd error: %s' % e)
            self._ssh.close()
        except AuthenticationException: 
            self._ssh = None
            raise ConnectionError('连接失败，请确认用户名、密码、端口或密钥文件是否有效')
        except Exception as e:
            self._ssh = None
            raise ConnectionError('remote connect error: %s' % e)

if __name__ == "__main__":
    update=Update()
    update.handle_files()
    update.transport()
    update.operate_remote(exchange_db=False)