import request from 'umi-request';
import { TableListParams, TableListItem } from './data.d';

export async function queryStaff(params?: TableListParams) {
  return request('/api/staff/query', {
    params,
  });
}

export async function addStaff(params: TableListItem) {
  return request('/api/staff/add', {
    method: 'POST',
    data: {
      ...params,
      method: 'post',
    },
  });
}
