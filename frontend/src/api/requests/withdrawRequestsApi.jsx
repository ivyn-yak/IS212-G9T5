import axios from 'axios';
import config from '../../config/config';

const BASE_URL = config.ENDPOINT_BE_URL;

export const getTeamPendingWithdrawals = async (managerId) => {
  try {
    console.log(`${BASE_URL}/api/team-manager/${managerId}/pending-requests-withdraw`);
    const response = await axios.get(`${BASE_URL}/api/team-manager/${managerId}/pending-requests-withdraw`);
    console.log(response);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const processWithdrawalDecision = async (payload) => {
  try {
    const response = await axios.post(`${BASE_URL}/api/approve_withdrawal`, payload);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Failed to process withdrawal decision');
    }
    throw error;
  }
};