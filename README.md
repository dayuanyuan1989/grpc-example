# grpc 双向流示例代码

期望实现类似于golang那种，send和recv分别处理，没有依赖

## HOW-TO-USE

```bash
pip install grpcio #gRPC 的安装 
pip install protobuf  #ProtoBuf 相关的 python 依赖库
pip install grpcio-tools   #python grpc 的 protobuf 编译工具

python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./chat.proto 

# 启动server
python3 server_async.py

# 启动client
python3 client_async.py
```

## TODO

- [ ] async server 实现send和recv分别处理

## 遇到的问题

grpc双向流，服务端同步方法只能通过yeild实现数据的返回，这就意味必须先收到数据，才能使用yeild发送数据

当然你可以在收到数据后，使用一个while 循环，然后在内部加一个yeild触发来在循环里触发，但是这会引入一个新问题，就是recv的时候数据会丢失

想要彻底分离读写依赖，只能通过python的异步的方式去解决

在python工程中，我们实际使用的场景是同步加线程，现在又引入同步，整个实现方式变得复杂，远远超出我预想的，类似于golang的routine的方式去实现
