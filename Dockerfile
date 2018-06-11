FROM registry.cn-hangzhou.aliyuncs.com/xiaoer_docker/python2
MAINTAINER Dick
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN touch /tmp/flushdb.log
HEALTHCHECK --interval=5s --timeout=1s \
	CMD pgrep -x supervisord
CMD supervisord -c supervisor.conf && tail -f /tmp/flushdb.log

