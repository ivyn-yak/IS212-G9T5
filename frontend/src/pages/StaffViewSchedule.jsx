import React, { useEffect } from 'react';
import WeeklySchedule from '../components/WeeklyCalendar/WeeklyCalendar';

function StaffViewSchedule() {
  useEffect(() => {
    console.log('StaffViewSchedule rendered');
  }, []);

  return (
    <div>
      <WeeklySchedule />
    </div>
  );
}

export default StaffViewSchedule;