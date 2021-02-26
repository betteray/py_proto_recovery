# PyProtoRecovery

Recover proto from compiled proto for python2.

### Usage
Find the compiled binary in xxxx_pb2.py's **serialized_pb**, eg:

```
DESCRIPTOR = _descriptor.FileDescriptor(
  name='e2e.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb= ...
```
Then, just replace **serialized_pb** in [main.py](https://github.com/betteray/py_proto_recovery/blob/31495274fa9fb12ca739043b22c2aa39b3623654/main.py#L97).

### Project Structure

```
├── README.md
├── descriptor.proto    // copy from https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/descriptor.proto
├── descriptor_pb2.py   // protoc --proto_path ./ --python_out=./ descriptor.proto
├── main.py             // main file for recovery
├── requirements.txt
```