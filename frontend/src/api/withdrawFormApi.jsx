// src/api/wfhRequests.js
import { format, subWeeks, addWeeks } from 'date-fns';
import config from '../config/config';

const BASE_URL = config.ENDPOINT_BE_URL;

export const getShiftType = (is_am, is_pm) => {
  if (is_am && is_pm) return "Full Day";
  if (is_am) return "AM Shift";
  if (is_pm) return "PM Shift";
  return "Unknown";
};

export const fetchApprovedSchedules = async (staffId) => {
  try {
    const today = new Date();
    const startDate = format(subWeeks(today, 2), 'yyyy-MM-dd');
    const endDate = format(addWeeks(today, 2), 'yyyy-MM-dd');

    const response = await fetch(
      `${BASE_URL}/api/staff/${staffId}/wfh_requests?start_date=${startDate}&end_date=${endDate}`
    );

    const data = await response.json();
    
    if (response.status === 404 || data.length === 0) {
      return {
        data: [],
        error: 'You have no approved requests to withdraw'
      };
    }
    
    if (!response.ok) {
      return {
        data: [],
        error: 'Failed to fetch approved schedules'
      };
    }

    const transformedData = data.map(schedule => ({
      ...schedule,
      id: schedule.request_id,
      type: getShiftType(schedule.is_am, schedule.is_pm)
    }));

    return {
      data: transformedData,
      error: null
    };
  } catch (error) {
    return {
      data: [],
      error: 'Failed to fetch approved schedules'
    };
  }
};

export const submitWithdrawal = async ({ request_id, reason, specific_date }) => {
  try {
    const response = await fetch(`${BASE_URL}/api/withdraw`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        request_id,
        reason,
        specific_date
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        error: data.error || 'Failed to submit withdrawal'
      };
    }

    return {
      success: true,
      error: null
    };
  } catch (error) {
    return {
      success: false,
      error: 'Failed to submit withdrawal'
    };
  }
};