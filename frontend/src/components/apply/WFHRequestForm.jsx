import React, { useState } from 'react';

const WFHRequestForm = () => {
  // State to manage form inputs
  const [formData, setFormData] = useState({
    type: 'Ad-hoc',        // Default to 'Ad-hoc'
    start_date: '',
    end_date: '',
    is_am: 0,              // AM checkbox (0 for no, 1 for yes)
    is_pm: 0,              // PM checkbox (0 for no, 1 for yes)
    reason: '',
    repeat_days: [],        // For recurring WFH requests
  });

  // Handle form input changes for checkboxes (convert true/false to 1/0)
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? (checked ? 1 : 0) : value,  // Convert true/false to 1/0 for checkboxes
    });
  };

  // Handle the repeat days for recurring requests
  const handleRepeatDays = (day) => {
    setFormData((prevState) => ({
      ...prevState,
      repeat_days: prevState.repeat_days.includes(day)
        ? prevState.repeat_days.filter((d) => d !== day)
        : [...prevState.repeat_days, day],
    }));
  };

  // Function to generate all recurring dates based on the selected start_date, end_date, and repeat_days
  const generateRecurringDates = (startDate, endDate, repeatDays) => {
    const recurringDates = [];
    const current = new Date(startDate);
    const end = new Date(endDate);
    
    while (current <= end) {
      const day = current.getDay(); // Get the current day of the week (0-6, where 0 is Sunday)
      
      // Check if the current day matches any of the selected repeatDays
      if (repeatDays.includes(day)) {
        recurringDates.push(new Date(current)); // Add to the list of recurring dates
      }
      
      // Move to the next day
      current.setDate(current.getDate() + 1);
    }
    
    return recurringDates;
  };

  // Form submission logic
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Generate all recurring dates if the request is of type 'Recurring'
    let recurringDates = [];
    if (formData.type === 'Recurring') {
      const repeatDays = formData.repeat_days.map(day => {
        // Map day names to numbers (e.g., 'M' = 1 for Monday)
        const dayMapping = { 'S': 0, 'M': 1, 'T': 2, 'W': 3, 'T': 4, 'F': 5, 'S': 6 };
        return dayMapping[day];
      });

      recurringDates = generateRecurringDates(formData.start_date, formData.end_date, repeatDays);
    }

    // Prepare payload for WFHRequests table
    const finalPayload = {
      ...formData,
      request_type: formData.type,  // Change 'type' to 'request_type'
      end_date: formData.type === 'Ad-hoc' ? formData.start_date : formData.end_date,
      staff_id: 1,
      apply_date: new Date().toISOString().split('T')[0],
    };
    

    console.log("Payload for WFHRequests:", finalPayload);

    try {
      // Submit the WFH request to the WFHRequests table
      const response = await fetch('http://localhost:5001/api/apply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(finalPayload),
      });

      const result = await response.json();
      if (response.ok) {
        console.log('WFH request submitted successfully!');
        
        // Now submit each recurring date to WFHRequestDates table
        for (const date of recurringDates) {
          const datePayload = {
            request_id: result.request_id, // Assuming the WFH request returns the request_id
            specific_date: date.toISOString().split('T')[0], // Convert date to YYYY-MM-DD format
            is_am: formData.is_am,
            is_pm: formData.is_pm,
            staff_id: formData.staff_id,
          };

          console.log("Payload for WFHRequestDates:", datePayload);

          await fetch('http://localhost:5001/api/wfhdates', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(datePayload),
          });
        }

        // After WFH request is created, add to RequestDecisions table
        await handleDecisionSubmit(result.request_id);
        alert('All recurring WFH dates submitted successfully!');
      } else {
        alert(`Error: ${result.error}`);
      }
    } catch (error) {
      console.error('Error submitting request:', error);
    }
  };

  // Function to handle adding a record to the RequestDecisions table
  const handleDecisionSubmit = async (requestId) => {
    const decisionPayload = {
      request_id: requestId,
      manager_id: 1, // Replace with actual manager ID
      decision_date: new Date().toISOString().split('T')[0], // Today's date
      decision_status: "pending", // Initial decision is "pending"
      decision_notes: "Awaiting manager approval" // Optional notes
    };

    console.log("Payload for RequestDecisions:", decisionPayload);

    try {
      const decisionResponse = await fetch('http://localhost:5001/api/request-decisions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(decisionPayload),
      });

      if (decisionResponse.ok) {
        console.log('Decision entry created successfully!');
      } else {
        console.error('Error submitting decision entry');
      }
    } catch (error) {
      console.error('Error creating decision entry:', error);
    }
  };

  return (
    <div className="wfh-request-container" style={{ padding: '20px' }}>
      <h2>Apply Work from Home Arrangement</h2>
      <form onSubmit={handleSubmit}>

        {/* Select Type of Arrangement */}
        <div>
          <label>Select type of arrangement</label>
          <select
            name="type"
            value={formData.type}
            onChange={handleInputChange}
            style={{ padding: '8px', marginBottom: '15px' }}
          >
            <option value="Ad-hoc">Ad-hoc</option>
            <option value="Recurring">Recurring</option>
          </select>
        </div>

        {/* For Ad-hoc Requests */}
        {formData.type === 'Ad-hoc' && (
          <>
            {/* Select Date */}
            <div>
              <label>Select Date</label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleInputChange}
                style={{ padding: '8px', marginBottom: '15px' }}
              />
            </div>
          </>
        )}

        {/* For Recurring Requests */}
        {formData.type === 'Recurring' && (
          <>
            {/* Select Start and End Dates */}
            <div>
              <label>Select Start date</label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleInputChange}
                style={{ padding: '8px', marginBottom: '15px' }}
              />
            </div>
            <div>
              <label>Select End date</label>
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleInputChange}
                style={{ padding: '8px', marginBottom: '15px' }}
              />
            </div>

            {/* Select Repeat Days */}
            <div>
              <label>Repeat on:</label>
              <div>
                {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleRepeatDays(day)}
                    style={{
                      margin: '5px',
                      padding: '10px',
                      backgroundColor: formData.repeat_days.includes(day)
                        ? '#007bff'
                        : '#ccc',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '50%',
                    }}
                  >
                    {day}
                  </button>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Select Timing */}
        <div>
          <label>Select Timing</label>
          <div>
            <label>
              <input
                type="checkbox"
                name="is_am"
                checked={formData.is_am === 1}
                onChange={handleInputChange}
              />
              AM
            </label>
            <label style={{ marginLeft: '20px' }}>
              <input
                type="checkbox"
                name="is_pm"
                checked={formData.is_pm === 1}
                onChange={handleInputChange}
              />
              PM
            </label>
          </div>
        </div>

        {/* Reason for WFH */}
        <div>
          <label>Please state reason for work from home arrangement</label>
          <textarea
            name="reason"
            value={formData.reason}
            onChange={handleInputChange}
            style={{ width: '100%', padding: '8px', marginTop: '10px' }}
          />
        </div>

        {/* Submit Button */}
        <button type="submit" style={{ padding: '10px 20px', marginTop: '20px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '5px' }}>
          Submit
        </button>
      </form>
    </div>
  );
};

export default WFHRequestForm;



