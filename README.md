# 弹弹play资源搜索节点API

### Using Docker Commands
```
docker run -d \
  -p 8080:8080 --name=dandan_api --restart=always \
  illyathehath/dandan-api
```

### Using Docker Compose
```
version: "3"
services:
  dandan:
    image: illyathehath/dandan-api
    # build: .
    restart: always
    ports:
      - "8080:8080"
```

在此只做了docker的封装，api的实现取自 https://pastebin.ubuntu.com/p/mGP7JRpBtd/ , 修改过安卓搜索bug的版本：https://pastebin.ubuntu.com/p/b33zZ3pvVr/
