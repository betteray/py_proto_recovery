# coding=utf-8

from google.protobuf import descriptor_pb2

def getLabel(label):
    if label == descriptor_pb2.FieldDescriptorProto.LABEL_OPTIONAL:
       return "optional"
    elif label == descriptor_pb2.FieldDescriptorProto.LABEL_REQUIRED:
        return "required"
    elif label == descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED:
        return "repeated"

def getType(type):
    if type == descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE:
        return "double"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT:
        return "float"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_INT64:
        return "int64"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_UINT64:
        return "uint64"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_INT32:
        return "int32"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_FIXED64:
        return "fixed64"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_FIXED32:
        return "fixed32"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_BOOL:
        return "bool"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_STRING:
        return "string"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_GROUP:
        return "group"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE:
        return "message"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_BYTES:
        return "bytes"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_UINT32:
        return "uint32"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_ENUM:
        return "enum"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_SFIXED32:
        return "sfixed32"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_SFIXED64:
        return "sfixed64"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_SINT32:
        return "sint32"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_SINT64:
        return "sint64"
    elif type == descriptor_pb2.FieldDescriptorProto.TYPE_SFIXED64:
        return "sfixed64"

def getMessageProto(message):
    result = "message " + message.name + " {\n"

    # enum type in this message
    for etype in message.enum_type:
        enumMessage = "enum " + etype.name + " {\n"
        for e in etype.value:
            enumMessage = enumMessage + "\t{0} = {1};\n".format(e.name, e.number)
        enumMessage = enumMessage + "}\n\n";
        result = result + enumMessage

    # nested_type in this message
    for ntypeMessage in message.nested_type:
        subMessage = getMessageProto(ntypeMessage)
        result = result + subMessage

    # this message fields
    for field in message.field:
        t = getType(field.type)
        if t == "message":
            t = field.type_name.split(".")[-1]
        elif t == "enum":
            t = field.type_name.split(".")[-1]
        result = result + "\t{0} {1} {2} = {3};\n".format(getLabel(field.label), t, field.name, field.number)

    return result + "}\n\n"

def do_recovery(buf):
    file_proto = descriptor_pb2.FileDescriptorProto()
    file_proto.ParseFromString(buf)

    print("// " + file_proto.name + "\n")
    print("syntax = \"proto2\";\n")

    for message in file_proto.message_type:
        messageProto = getMessageProto(message)
        print(messageProto)

def recover(bin_path_name):
    with open(bin_path_name, "rb") as f:
        buf = f.read()
        do_recovery(buf)

if __name__ == '__main__':
    serialized_pb=b'\n\nwa20.proto\"\x97\x11\n\rClientPayload\x12\x10\n\x08username\x18\x01 \x01(\x04\x12\x0f\n\x07passive\x18\x03 \x01(\x08\x12\x35\n\x0f\x63lient_features\x18\x04 \x03(\x0e\x32\x1c.ClientPayload.ClientFeature\x12,\n\nuser_agent\x18\x05 \x01(\x0b\x32\x18.ClientPayload.UserAgent\x12(\n\x08web_info\x18\x06 \x01(\x0b\x32\x16.ClientPayload.WebInfo\x12\x11\n\tpush_name\x18\x07 \x01(\t\x12\x12\n\nsession_id\x18\t \x01(\x0f\x12\x15\n\rshort_connect\x18\n \x01(\x08\x12\x30\n\x0c\x63onnect_type\x18\x0c \x01(\x0e\x32\x1a.ClientPayload.ConnectType\x12\x34\n\x0e\x63onnect_reason\x18\r \x01(\x0e\x32\x1c.ClientPayload.ConnectReason\x12\x0e\n\x06shards\x18\x0e \x03(\x0f\x12,\n\ndns_source\x18\x0f \x01(\x0b\x32\x18.ClientPayload.DnsSource\x12\x1d\n\x15\x63onnect_attempt_count\x18\x10 \x01(\x0f\x12\x39\n\x11ios_app_extension\x18\x1e \x01(\x0e\x32\x1e.ClientPayload.IosAppExtension\x1a\x9a\x01\n\tDnsSource\x12\x35\n\tdnsMethod\x18\x0f \x01(\x0e\x32\".ClientPayload.DnsSource.DnsMethod\x12\x11\n\tappCached\x18\x10 \x01(\x08\"C\n\tDnsMethod\x12\x0c\n\x08METHOD_0\x10\x00\x12\x0c\n\x08METHOD_1\x10\x01\x12\x0c\n\x08METHOD_2\x10\x02\x12\x0c\n\x08METHOD_3\x10\x03\x1a\xeb\x05\n\tUserAgent\x12<\n\x08platform\x18\x01 \x01(\x0e\x32!.ClientPayload.UserAgent.Platform:\x07\x41NDROID\x12\x38\n\x0b\x61pp_version\x18\x02 \x01(\x0b\x32#.ClientPayload.UserAgent.AppVersion\x12\x0b\n\x03mcc\x18\x03 \x01(\t\x12\x0b\n\x03mnc\x18\x04 \x01(\t\x12\x12\n\nos_version\x18\x05 \x01(\t\x12\x14\n\x0cmanufacturer\x18\x06 \x01(\t\x12\x0e\n\x06\x64\x65vice\x18\x07 \x01(\t\x12\x17\n\x0fos_build_number\x18\x08 \x01(\t\x12\x10\n\x08phone_id\x18\t \x01(\t\x12I\n\x0frelease_channel\x18\n \x01(\x0e\x32\'.ClientPayload.UserAgent.ReleaseChannel:\x07RELEASE\x12!\n\x19locale_language_iso_639_1\x18\x0b \x01(\t\x12)\n!locale_country_iso_3166_1_alpha_2\x18\x0c \x01(\t\x1aV\n\nAppVersion\x12\x0f\n\x07primary\x18\x01 \x01(\r\x12\x11\n\tsecondary\x18\x02 \x01(\r\x12\x10\n\x08tertiary\x18\x03 \x01(\r\x12\x12\n\nquaternary\x18\x04 \x01(\r\"\xb6\x01\n\x08Platform\x12\x0b\n\x07\x41NDROID\x10\x00\x12\x07\n\x03IOS\x10\x01\x12\x11\n\rWINDOWS_PHONE\x10\x02\x12\x0e\n\nBLACKBERRY\x10\x03\x12\x0f\n\x0b\x42LACKBERRYX\x10\x04\x12\x07\n\x03S40\x10\x05\x12\x07\n\x03S60\x10\x06\x12\x11\n\rPYTHON_CLIENT\x10\x07\x12\t\n\x05TIZEN\x10\x08\x12\x0e\n\nENTERPRISE\x10\t\x12\x0f\n\x0bPLATFORM_10\x10\n\x12\x0f\n\x0bPLATFORM_11\x10\x0b\"=\n\x0eReleaseChannel\x12\x0b\n\x07RELEASE\x10\x00\x12\x08\n\x04\x42\x45TA\x10\x01\x12\t\n\x05\x41LPHA\x10\x02\x12\t\n\x05\x44\x45\x42UG\x10\x03\x1a\xa7\x03\n\x07WebInfo\x12\x11\n\tref_token\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x38\n\x0cwebd_payload\x18\x03 \x01(\x0b\x32\".ClientPayload.WebInfo.WebdPayload\x1a\xbd\x02\n\x0bWebdPayload\x12\x1f\n\x17uses_participant_in_key\x18\x01 \x01(\x08\x12!\n\x19supports_starred_messages\x18\x02 \x01(\x08\x12\"\n\x1asupports_document_messages\x18\x03 \x01(\x08\x12\x1d\n\x15supports_url_messages\x18\x04 \x01(\x08\x12\x1c\n\x14supports_media_retry\x18\x05 \x01(\x08\x12\x1a\n\x12supports_e2e_image\x18\x06 \x01(\x08\x12\x1a\n\x12supports_e2e_video\x18\x07 \x01(\x08\x12\x1a\n\x12supports_e2e_audio\x18\x08 \x01(\x08\x12\x1d\n\x15supports_e2e_document\x18\t \x01(\x08\x12\x16\n\x0e\x64ocument_types\x18\n \x01(\t\"\x19\n\rClientFeature\x12\x08\n\x04NONE\x10\x00\"\xac\x01\n\x0b\x43onnectType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04WIFI\x10\x01\x12\x08\n\x04\x45\x44GE\x10\x64\x12\x08\n\x04IDEN\x10\x65\x12\x08\n\x04UMTS\x10\x66\x12\x08\n\x04\x45VDO\x10g\x12\x08\n\x04GPRS\x10h\x12\t\n\x05HSDPA\x10i\x12\t\n\x05HSUPA\x10j\x12\x08\n\x04HSPA\x10k\x12\x08\n\x04\x43\x44MA\x10l\x12\x0b\n\x07ONExRTT\x10m\x12\t\n\x05\x45HRPD\x10n\x12\x07\n\x03LTE\x10o\x12\t\n\x05HSPAP\x10p\"c\n\rConnectReason\x12\x0c\n\x08REASON_0\x10\x00\x12\x0c\n\x08REASON_1\x10\x01\x12\x0c\n\x08REASON_2\x10\x02\x12\x0c\n\x08REASON_3\x10\x03\x12\x0c\n\x08REASON_4\x10\x04\x12\x0c\n\x08REASON_5\x10\x06\"2\n\x0fIosAppExtension\x12\t\n\x05\x45XT_0\x10\x00\x12\t\n\x05\x45XT_1\x10\x01\x12\t\n\x05\x45XT_2\x10\x02\"\xea\x02\n\x10HandshakeMessage\x12\x33\n\x0c\x63lient_hello\x18\x02 \x01(\x0b\x32\x1d.HandshakeMessage.ClientHello\x12\x33\n\x0cserver_hello\x18\x03 \x01(\x0b\x32\x1d.HandshakeMessage.ServerHello\x12\x35\n\rclient_finish\x18\x04 \x01(\x0b\x32\x1e.HandshakeMessage.ClientFinish\x1a\x41\n\x0b\x43lientHello\x12\x11\n\tephemeral\x18\x01 \x01(\x0c\x12\x0e\n\x06static\x18\x02 \x01(\x0c\x12\x0f\n\x07payload\x18\x03 \x01(\x0c\x1a\x41\n\x0bServerHello\x12\x11\n\tephemeral\x18\x01 \x01(\x0c\x12\x0e\n\x06static\x18\x02 \x01(\x0c\x12\x0f\n\x07payload\x18\x03 \x01(\x0c\x1a/\n\x0c\x43lientFinish\x12\x0e\n\x06static\x18\x01 \x01(\x0c\x12\x0f\n\x07payload\x18\x02 \x01(\x0c\"\x90\x01\n\x10NoiseCertificate\x12\x0f\n\x07\x64\x65tails\x18\x01 \x01(\x0c\x12\x11\n\tsignature\x18\x02 \x01(\x0c\x1aX\n\x07\x44\x65tails\x12\x0e\n\x06serial\x18\x01 \x01(\r\x12\x0e\n\x06issuer\x18\x02 \x01(\t\x12\x0f\n\x07\x65xpires\x18\x03 \x01(\x04\x12\x0f\n\x07subject\x18\x04 \x01(\t\x12\x0b\n\x03key\x18\x05 \x01(\x0c'
    do_recovery(serialized_pb)
    # recover("/path/to/xxxx_pb2.descriptor_pb2.bin") # descriptor_pb2 bytes
