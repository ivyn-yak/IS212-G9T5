import React, { useEffect } from 'react';
import WeeklySchedule from '../components/WeeklyCalendar/WeeklyCalendar';

function ManageerViewTeamSchedule() {
  useEffect(() => {
    console.log('ManageerViewTeamSchedule rendered');
  }, []);

  return (
    <div>
      <WeeklySchedule />
    </div>
  );
}

export default ManageerViewTeamSchedule;