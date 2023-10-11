#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'cloudkdb'

"""
阿里云数据订阅功能 Python Demo
Aliyun data subscribe Python Demo
"""

import io
import pprint
import avro.schema
from kafka import KafkaConsumer
from avro.io import DatumReader, BinaryDecoder

with open("Record.avsc") as avsc_file:
    avsc = avsc_file.read()
    schema = avro.schema.parse(avsc)
    reader = DatumReader(schema)

def deserialize(reader, msg):
    message_bytes = io.BytesIO(msg)
    decoder = BinaryDecoder(message_bytes)
    event_dict = reader.read(decoder)
    return event_dict

try:
    """ 参数说明
    第一个参数是订阅 Topic 名称，DTS-数据订阅-基本信息 可查
    group_id: 消费组ID，DTS-数据订阅-数据消费 可查
    sasl_plain_username: 创建消费组的账号
    sasl_plain_sasl_plain_password: 创建消费组的密码
    bootstrap_servers: 数据订阅通道地址，DTS-数据订阅-基本信息-网络部分，可以查到
    """
    consumer = KafkaConsumer('topic',
                            group_id="group_id",
                            sasl_mechanism="PLAIN",
                            security_protocol='SASL_PLAINTEXT',
                            sasl_plain_username="user",
                            sasl_plain_password="password",
                            bootstrap_servers='server:port')
    print("start subscribe msg.")
    for msg in consumer:
        print("---------------------------------")
        pprint.pprint(deserialize(reader, msg.value), indent=4)
        print("---------------------------------\n")
except Exception as e:
    print(e)



"""

output:

1. Insert MSG
{   'afterImages': [   {'precision': 8, 'value': '123456789'},
                       {   'charset': 'utf8mb4',
                           'value': b'test insert statement.'}],
    'beforeImages': None,
    'bornTimestamp': 1696984408,
    'fields': [   {'dataTypeNumber': 8, 'name': 'a'},
                  {'dataTypeNumber': 253, 'name': 'b'}],
    'id': 1700382,
    'objectName': 'mydb.t1',
    'operation': 'INSERT',
    'processTimestamps': None,
    'safeSourcePosition': '72347@78',
    'source': {'sourceType': 'MySQL', 'version': '8.0.28'},
    'sourcePosition': '72469@78',
    'sourceTimestamp': 1696984408,
    'sourceTxid': '0',
    'tags': {   'metaVersion': '3109599372',
                'pk_uk_info': '{"PRIMARY":["a"]}',
                'readerThroughoutTime': '1696984408050',
                'server_id': '26957161',
                'thread_id': '163931'},
    'version': 0}

2. Update MSG
{   'afterImages': [   {'precision': 8, 'value': '123456789'},
                       {   'charset': 'utf8mb4',
                           'value': b'test update statement.'}],
    'beforeImages': [   {'precision': 8, 'value': '123456789'},
                        {   'charset': 'utf8mb4',
                            'value': b'test insert statement.'}],
    'bornTimestamp': 1696984517,
    'fields': [   {'dataTypeNumber': 8, 'name': 'a'},
                  {'dataTypeNumber': 253, 'name': 'b'}],
    'id': 1700504,
    'objectName': 'mydb.t1',
    'operation': 'UPDATE',
    'processTimestamps': None,
    'safeSourcePosition': '75103@78',
    'source': {'sourceType': 'MySQL', 'version': '8.0.28'},
    'sourcePosition': '75259@78',
    'sourceTimestamp': 1696984517,
    'sourceTxid': '0',
    'tags': {   'metaVersion': '3109599372',
                'pk_uk_info': '{"PRIMARY":["a"]}',
                'readerThroughoutTime': '1696984517078',
                'server_id': '26957161',
                'thread_id': '163931'},
    'version': 0}

3. Delete MSG
{   'afterImages': None,
    'beforeImages': [   {'precision': 8, 'value': '123456789'},
                        {   'charset': 'utf8mb4',
                            'value': b'test update statement.'}],
    'bornTimestamp': 1696984560,
    'fields': [   {'dataTypeNumber': 8, 'name': 'a'},
                  {'dataTypeNumber': 253, 'name': 'b'}],
    'id': 1700553,
    'objectName': 'mydb.t1',
    'operation': 'DELETE',
    'processTimestamps': None,
    'safeSourcePosition': '76054@78',
    'source': {'sourceType': 'MySQL', 'version': '8.0.28'},
    'sourcePosition': '76176@78',
    'sourceTimestamp': 1696984560,
    'sourceTxid': '0',
    'tags': {   'metaVersion': '3109599372',
                'pk_uk_info': '{"PRIMARY":["a"]}',
                'readerThroughoutTime': '1696984560421',
                'server_id': '26957161',
                'thread_id': '163931'},
    'version': 0}

4. DDL
{   'afterImages': 'create table t1(a bigint primary key, b varchar(100))',
    'beforeImages': None,
    'bornTimestamp': 1696984152,
    'fields': None,
    'id': 1700104,
    'objectName': 'mydb',
    'operation': 'DDL',
    'processTimestamps': None,
    'safeSourcePosition': '67008@78',
    'source': {'sourceType': 'MySQL', 'version': '8.0.28'},
    'sourcePosition': '67008@78',
    'sourceTimestamp': 1696984152,
    'sourceTxid': '0',
    'tags': {   'GTID': '281c62dc-590c-11ee-a295-00163e390c7c:108156',
                'GTID_SET': '281c62dc-590c-11ee-a295-00163e390c7c:1-108156',
                'Q_CHARSET_CODE': '33',
                'Q_FLAGS2_CODE': '0',
                'Q_SQL_MODE_CODE': '1168113696',
                'commitTimestamp': '1696984152',
                'lowerCaseTableNames': 'true',
                'readerThroughoutTime': '1696984152751',
                'server_id': '26957161',
                'thread_id': '163931'},
    'version': 0}

"""
