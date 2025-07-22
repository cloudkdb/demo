#!/bin/bash

show_menu() {
    echo "====================="
    echo "     MongoDB 工具      "
    echo "====================="
    echo "1. 创建 MongoDB 实例"
    echo "2. 查看 MongoDB 实例列表"
    echo "3. 查看 MongoDB 实例详情"
    echo "q. 退出"
    echo "====================="
}

# 安装阿里云CLI：https://help.aliyun.com/zh/cli/install-cli-on-linux
# 配置aliyun cli: https://help.aliyun.com/zh/cli/configure-credentials

create() {
# 引入通用配置文件
source ./mongodb_common.conf
read -p "请输入包月还是按量(包月请输入:PrePaid；按量请输入：PostPaid)：" paid_type 
ChargeType="${paid_type}"

read -p "请输入MongoDB实例名称：" name 
DBInstanceDescription="${name}"

echo "Create MongoDB Instance..."
aliyun dds CreateDBInstance \
  --DBInstanceDescription="${DBInstanceDescription}" \
  --RegionId="${RegionId}" \
  --ZoneId="${ZoneId}" \
  --SecondaryZoneId="${SecondaryZoneId}" \
  --HiddenZoneId="${HiddenZoneId}" \
  --EngineVersion="${EngineVersion}" \
  --DBInstanceClass="${DBInstanceClass}" \
  --StorageType="${StorageType}" \
  --DBInstanceStorage=${DBInstanceStorage} \
  --VpcId="${VpcId}" \
  --VSwitchId="${VSwitchId}" \
  --AccountPassword="${AccountPassword}" \
  --ChargeType="${ChargeType}" \
  --Period=${Period} \
  --AutoRenew="${AutoRenew}" \
  --read-timeout="${ReadTimeout}" \
  --connect-timeout="${ConnectTimeout}"

    sleep 1
}

list() {
    echo "List MongoDB Instances..."
    aliyun dds DescribeDBInstances
}

desc() {
    read -p "输入MongoDB实例ID: " mongodb_id 
    echo "Describe MongoDB Instance..."
    aliyun dds DescribeDBInstanceAttribute --DBInstanceId "${mongodb_id}"
    sleep 1
}

while true; do
    show_menu
    read -p "请输入选项 (1-3 或 q): " choice

    case $choice in
        1)
            create
            ;;
        2)
            list
            ;;
        3)
            desc
            ;;
        q|Q)
            echo "退出"
            exit 0
            ;;
        *)
            echo "无效选项，请重新输入。"
            sleep 1
            ;;
    esac
done
