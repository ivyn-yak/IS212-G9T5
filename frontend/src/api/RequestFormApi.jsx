// src/api/wfhRequests.js
import config from '../config/config';

const BASE_URL = config.ENDPOINT_BE_URL;

export const dayMapping = {
  'Mon': 'monday',
  'Tue': 'tuesday',
  'Wed': 'wednesday',
  'Thu': 'thursday',
  'Fri': 'friday',
  'Sat': 'saturday',
  'Sun': 'sunday'
};

export const submitWFHRequest = async (formData) => {
  try {
    const payload = {
      staff_id: formData.staff_id,
      request_type: formData.request_type,
      start_date: formData.start_date,
      end_date: formData.request_type === 'Ad-hoc' ? formData.start_date : formData.end_date,
      recurrence_days: formData.request_type === 'Recurring' ? 
        dayMapping[formData.recurrence_days] || formData.recurrence_days : null,
      is_am: formData.is_am,
      is_pm: formData.is_pm,
      apply_date: formData.apply_date,
      request_reason: formData.request_reason
    };

    const response = await fetch(`${BASE_URL}/api/apply`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
      credentials: 'include',
    });

    const data = await response.json();
    
    return {
      success: response.ok,
      data: response.ok ? data : null,
      error: response.ok ? null : (data.error || 'Failed to submit request')
    };
  } catch (error) {
    return {
      success: false,
      data: null,
      error: 'Failed to submit request. Please try again.'
    };
  }
};