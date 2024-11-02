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