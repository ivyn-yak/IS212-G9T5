// api/scheduleApi.js
export const fetchManagerSchedule = async (managerId, startDate, endDate) => {
    try {
      // First fetch team members
      const teamResponse = await fetch(`http://localhost:5001/api/team/${managerId}`);
      if (!teamResponse.ok) {
        throw new Error(`Error fetching team data: ${teamResponse.status}`);
      }
      const teamMembers = await teamResponse.json();
  
      // Then fetch WFH schedule
      const scheduleResponse = await fetch(
        `http://localhost:5001/api/manager/${managerId}/team_schedule?start_date=${startDate}&end_date=${endDate}`
      );
      
      let scheduleData = {};
      if (scheduleResponse.status === 404) {
        // If no WFH data, create default schedule with everyone in office
        scheduleData = {
          staff: {
            staff_id: managerId,
            ScheduleDetails: []
          },
          team: []
        };
      } else if (scheduleResponse.ok) {
        scheduleData = await scheduleResponse.json();
      } else {
        throw new Error(`Error fetching schedule data: ${scheduleResponse.status}`);
      }
  
      // Combine team data with schedule data
      return {
        staff: {
          staffID: scheduleData.staff.staff_id,
          name: teamMembers.find(m => m.staff_id === parseInt(managerId))?.name,
          scheduleTrails: scheduleData.staff.ScheduleDetails.map(detail => ({
            date: detail.specific_date,
            is_am: detail.is_am,
            is_pm: detail.is_pm
          }))
        },
        team: teamMembers.map(member => ({
          staffID: member.staff_id.toString(),
          name: member.name,
          scheduleTrails: (scheduleData.team.find(t => t.staff_id === member.staff_id)?.ScheduleDetails || [])
            .map(detail => ({
              date: detail.specific_date,
              is_am: detail.is_am,
              is_pm: detail.is_pm
            }))
        }))
      };
    } catch (error) {
      console.error('Error fetching manager schedule:', error);
      throw error;
    }
  };
  
  export const fetchStaffSchedule = async (staffId, startDate, endDate) => {
    try {
      // First fetch team members
      const teamResponse = await fetch(`http://localhost:5001/api/team/${staffId}`);
      if (!teamResponse.ok) {
        throw new Error(`Error fetching team data: ${teamResponse.status}`);
      }
      const teamMembers = await teamResponse.json();
  
      // Fetch staff's own WFH schedule
      const staffResponse = await fetch(
        `http://localhost:5001/api/staff/${staffId}/wfh_requests?start_date=${startDate}&end_date=${endDate}`
      );
      
      let staffSchedule = [];
      if (staffResponse.status === 404) {
        // If no data found, leave the schedule empty (meaning all office days)
        staffSchedule = [];
      } else if (staffResponse.ok) {
        const staffData = await staffResponse.json();
        console.log(staffData);
        staffSchedule = staffData.map(detail => ({
          date: detail.specific_date,
          is_am: detail.is_am,
          is_pm: detail.is_pm
        }));
      } else {
        throw new Error(`HTTP error! status: ${staffResponse.status}`);
      }
  
      // Fetch team's WFH schedule
      const teamScheduleResponse = await fetch(
        `http://localhost:5001/api/team/${staffId}/schedule?start_date=${startDate}&end_date=${endDate}`
      );
  
      let teamScheduleData = [];
      if (teamScheduleResponse.status === 404) {
        // If no team schedule data found, use empty array (meaning all office days)
        teamScheduleData = [];
      } else if (teamScheduleResponse.ok) {
        teamScheduleData = await teamScheduleResponse.json();
      } else {
        throw new Error(`HTTP error! status: ${teamScheduleResponse.status}`);
      }
  
      // Combine all data
      return {
        staff: {
          staffID: staffId,
          name: teamMembers.find(m => m.staff_id === parseInt(staffId))?.name,
          scheduleTrails: staffSchedule
        },
        team: teamMembers
          .filter(member => member.staff_id !== parseInt(staffId)) // Exclude current staff from team list
          .map(member => ({
            staffID: member.staff_id.toString(),
            name: member.name,
            scheduleTrails: (teamScheduleData.find(t => t.staff_id === member.staff_id)?.ScheduleDetails || [])
              .map(detail => ({
                date: detail.specific_date,
                is_am: detail.is_am,
                is_pm: detail.is_pm
              }))
          }))
      };
    } catch (error) {
      console.error('Error fetching staff schedule:', error);
      throw error;
    }
  };