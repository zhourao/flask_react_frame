import { PlusOutlined } from '@ant-design/icons';
import { PageHeaderWrapper } from '@ant-design/pro-layout';
import ProTable, { ActionType, ProColumns } from '@ant-design/pro-table';
import { Button, message } from 'antd';
import React, { useRef, useState } from 'react';
import CreateForm from './components/CreateForm';
import { TableListItem } from './data.d';
import { queryStaff, addStaff } from './service';


/**
 * 添加节点
 * @param fields
 */
const handleAdd = async (fields: TableListItem) => {
  const hide = message.loading('正在添加');
  try {
    await addStaff({ ...fields });
    hide();
    message.success('添加成功');
    return true;
  } catch (error) {
    hide();
    message.error('添加失败请重试！');
    return false;
  }
};

const TableList: React.FC<{}> = () => {
  const [createModalVisible, handleModalVisible] = useState<boolean>(false);
  const actionRef = useRef<ActionType>();
  const columns: ProColumns<TableListItem>[] = [
    {
      title: '昵称',
      dataIndex: 'nickname',
      rules: [
        {
          required: true,
          message: '昵称为必填项',
        },
      ],
    },
    {
      title: '登录名称',
      dataIndex: 'login_name',
      hideInSearch: true,
      rules: [
        {
          required: true,
          message: '登录名称为必填项',
        }, {
          pattern: /^[a-zA-Z0-9_]{3,20}$/,
          message: '登录名称必须英文开头，数据组合，且长度为3-20'
        }
      ],
    },
    {
      title: '登录密码',
      dataIndex: 'login_pwd',
      hideInSearch: true,
      hideInTable: true,
      rules: [
        {
          required: true,
          message: '请输入值'
        }, {
          pattern: /^[a-zA-Z0-9_*]{6,20}$/,
          message: '密码必须英文数据_*组合，且长度为6-20'
        }
      ],
    },
    {
      title: '性别',
      dataIndex: 'is_male',
      valueEnum: {
        0: { text: '女', status: '0' },
        1: { text: '男', status: '1' },
      },
      rules: [
        {
          required: true,
          message: '请选择值'
        }
      ],
    },
    {
      title: '手机号',
      dataIndex: 'mobile',
      hideInSearch: true,
      rules: [
        {
          required: true,
          message: '请输入值'
        }, {
          pattern: /^1[3-9]\d{9}$/,
          message: '手机号格式不正确'
        }
      ],
    },
    {
      title: '电子邮箱',
      dataIndex: 'email',
      hideInSearch: true,
      rules: [
        {
          pattern: /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
          message: '电子邮箱格式不正确'
        }
      ],
    },
    {
      title: '状态',
      dataIndex: 'status',
      hideInForm: true,
      valueEnum: {
        0: { text: '无效', status: '0' },
        1: { text: '有效', status: '1' },
      },
    },
    {
      title: '生日',
      name: 'birthday',
      valueType: 'dateTime',
      rules: [{
        required: true,
        message: '请输入值'
      }],
    },
    {
      title: '创建时间',
      dataIndex: 'created_time',
      hideInSearch: true,
      sorter: true,
      hideInForm: true,
    },
  ];

  return (
    <PageHeaderWrapper>
      <ProTable<TableListItem>
        headerTitle="成员管理"
        actionRef={actionRef}
        rowKey="key"
        toolBarRender={(action, { selectedRows }) => [
          <Button type="primary" onClick={() => handleModalVisible(true)}>
            <PlusOutlined /> 新建
          </Button>,
        ]}
        request={(params, sorter, filter) => queryStaff({ ...params, sorter, filter })}
        columns={columns}
      />
      <CreateForm onCancel={() => handleModalVisible(false)} modalVisible={createModalVisible}>
        <ProTable<TableListItem, TableListItem>
          onSubmit={async (value) => {
            const success = await handleAdd(value);
            if (success) {
              handleModalVisible(false);
              if (actionRef.current) {
                actionRef.current.reload();
              }
            }
          }}
          rowKey="key"
          type="form"
          columns={columns}
          rowSelection={{}}
        />
      </CreateForm>
    </PageHeaderWrapper>
  );
};

export default TableList;
