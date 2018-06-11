## 功能简介
自动扫描数据库,当发现有处于审核状态的请求后,就会向这些用户发送短信,提示其已经验证通过,
紧接着将所有处于审核状态的申请都转化为 审核通过状态.

## 使用说明
master是开发分支,release是当前线上运行的稳定分支。
### 开发环境
- 设置环境变量,或者编辑flushdb.py中的configs配置
```
export ETCD=10.8.100.100:2379
export APP_NAME=flushdb
```
- 安装依赖文件
```
pip install -r requirements
```
- 运行应用
```
python main.py
```

### 发布应用
- 运行docker build
```
docker build -t flushdb .
```
- 运行flushdb
```
docker run --rm -e ETCD=10.8.100.111:2379 -e APP_NAME=flushdb flushdb
```
