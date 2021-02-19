# HolyCA
## Server
```bash
cd server/caserver
source datavis/bin/activate
cd caserver
```
开发环境（在虚拟datavis环境中）:
```bash
python3 manage.py runserver
```
生产环境（在虚拟datavis环境中）:
```bash
nohup python manage.py runserver 0.0.0.0:8000>manage.log &
```
## Web
```bash
cd web/caweb
yarn serve
```
## Install Requirements
安装 requirement.txt 所包含的依赖:
```bash
pip install -r requirements.txt
```
把环境中的依赖写入 requirement.txt 中:
```bash
pip freeze >requirements.txt
```
## Stop Process
macos:
```bash
lsof -i:8000
kill -9 [PID]
```
linux:
```bash
netstat -ntlp |grep 8000
kill -9 [PID]
```
