// src/components/WFHRequestForm.jsx
import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { submitWFHRequest, dayMapping } from '../../api/RequestFormApi';
import { format, addMonths, subMonths } from 'date-fns';

const WFHRequestForm = () => {
  const { staffId } = useParams();

  const today = new Date();
  const minDate = format(subMonths(today, 2), 'yyyy-MM-dd');
  const maxDate = format(addMonths(today, 3), 'yyyy-MM-dd');

  const [formData, setFormData] = useState({
    staff_id: staffId,
    request_type: 'Ad-hoc',
    start_date: '',
    end_date: '',
    recurrence_days: '',
    is_am: false,
    is_pm: false,
    apply_date: format(today, 'yyyy-MM-dd'),
    request_reason: ''
  });

  const [errors, setErrors] = useState({});
  const [submitMessage, setSubmitMessage] = useState({ type: '', message: '' });

  const validateForm = () => {
    const newErrors = {};

    if (!formData.is_am && !formData.is_pm) {
      newErrors.timing = 'Please select at least one timing (AM/PM)';
    }

    if (formData.request_type === 'Recurring' && !formData.recurrence_days) {
      newErrors.recurrence_days = 'Please select a recurring day';
    }

    const startDate = new Date(formData.start_date);
    if (!formData.start_date) {
      newErrors.start_date = 'Please select a start date';
    } else if (startDate < new Date(minDate) || startDate > new Date(maxDate)) {
      newErrors.start_date = 'Start date must be within 2 months before and 3 months after current date';
    }

    if (formData.request_type === 'Recurring') {
      const endDate = new Date(formData.end_date);
      
      if (!formData.end_date) {
        newErrors.end_date = 'Please select an end date';
      } else if (endDate < new Date(minDate) || endDate > new Date(maxDate)) {
        newErrors.end_date = 'End date must be within 2 months before and 3 months after current date';
      } else if (endDate < startDate) {
        newErrors.date_range = 'End date must be after or equal to start date';
      }
    }

    if (!formData.request_reason.trim()) {
      newErrors.request_reason = 'Please provide a reason';
    }

    if (formData.request_type === 'Recurring' && formData.start_date && formData.end_date) {
      if (new Date(formData.end_date) < new Date(formData.start_date)) {
        newErrors.date_range = 'End date must be after start date';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    // For recurring requests, ensure end_date is not before start_date
    if (name === 'start_date' && formData.request_type === 'Recurring') {
      const newStartDate = new Date(value);
      const currentEndDate = new Date(formData.end_date);
      
      setFormData(prev => ({
        ...prev,
        [name]: value,
        // Reset end_date if it's before the new start_date
        end_date: currentEndDate < newStartDate ? value : prev.end_date
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value,
      }));
    }

    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleRecurrenceDay = (day) => {
    setFormData(prev => ({
      ...prev,
      recurrence_days: prev.recurrence_days === day ? '' : day
    }));
    if (errors.recurrence_days) {
      setErrors({ ...errors, recurrence_days: '' });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitMessage({ type: '', message: '' });

    if (!validateForm()) {
      setSubmitMessage({ 
        type: 'error', 
        message: 'Please correct the errors before submitting' 
      });
      return;
    }

    const response = await submitWFHRequest(formData);

    if (response.success) {
      setSubmitMessage({ 
        type: 'success', 
        message: 'WFH request submitted successfully!' 
      });
      // Reset form
      setFormData(prev => ({
        ...prev,
        start_date: '',
        end_date: '',
        recurrence_days: '',
        is_am: false,
        is_pm: false,
        request_reason: ''
      }));
    } else {
      setSubmitMessage({ 
        type: 'error', 
        message: response.error 
      });
    }
  };
  
  return (
    <div className="wfh-request-container" style={{ padding: '20px' }}>
      <h2>Apply Work from Home Arrangement</h2>
      
      {submitMessage.message && (
        <div 
          style={{ 
            padding: '10px', 
            marginBottom: '15px',
            backgroundColor: submitMessage.type === 'success' ? '#d4edda' : '#f8d7da',
            color: submitMessage.type === 'success' ? '#155724' : '#721c24',
            borderRadius: '4px'
          }}
        >
          {submitMessage.message}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Request Type Selection */}
        <div style={{ marginBottom: '15px' }}>
          <label>Select type of arrangement</label>
          <select
            name="request_type"
            value={formData.request_type}
            onChange={handleInputChange}
            style={{ padding: '8px', marginTop: '5px', width: '100%' }}
            required
          >
            <option value="Ad-hoc">Ad-hoc</option>
            <option value="Recurring">Recurring</option>
          </select>
        </div>

        {/* For Ad-hoc Requests */}
        {formData.request_type === 'Ad-hoc' && (
        <div style={{ marginBottom: '15px' }}>
          <label>Select Date</label>
          <input
            type="date"
            name="start_date"
            value={formData.start_date}
            onChange={handleInputChange}
            min={minDate}
            max={maxDate}
            style={{ padding: '8px', marginTop: '5px', width: '100%' }}
            required
          />
          {errors.start_date && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {errors.start_date}
            </div>
          )}
        </div>
      )}

        {/* For Recurring Requests */}
        {formData.request_type === 'Recurring' && (
        <>
          <div style={{ marginBottom: '15px' }}>
            <label>Select Start date</label>
            <input
              type="date"
              name="start_date"
              value={formData.start_date}
              onChange={handleInputChange}
              min={minDate}
              max={maxDate}
              style={{ padding: '8px', marginTop: '5px', width: '100%' }}
              required
            />
            {errors.start_date && (
              <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
                {errors.start_date}
              </div>
            )}
          </div>
          
          <div style={{ marginBottom: '15px' }}>
            <label>Select End date</label>
            <input
              type="date"
              name="end_date"
              value={formData.end_date}
              onChange={handleInputChange}
              min={formData.start_date || minDate}
              max={maxDate}
              style={{ padding: '8px', marginTop: '5px', width: '100%' }}
              required
            />
            {errors.end_date && (
              <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
                {errors.end_date}
              </div>
            )}
          </div>

          {errors.date_range && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginBottom: '15px' }}>
              {errors.date_range}
            </div>
          )}

            <div style={{ marginBottom: '15px' }}>
              <label>Select recurring day:</label>
              <div style={{ marginTop: '10px' }}>
                {Object.entries(dayMapping).map(([key, value]) => (
                  <button
                    key={key}
                    type="button"
                    onClick={() => handleRecurrenceDay(key)}
                    style={{
                      margin: '5px',
                      padding: '10px',
                      backgroundColor: formData.recurrence_days === key ? '#007bff' : '#ccc',
                      color: '#fff',
                      border: 'none',
                      borderRadius: '50%',
                      cursor: 'pointer'
                    }}
                  >
                    {key}
                  </button>
                ))}
              </div>
              {errors.recurrence_days && (
                <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
                  {errors.recurrence_days}
                </div>
              )}
            </div>
          </>
        )}

        {/* Timing Selection */}
        <div style={{ marginBottom: '15px' }}>
          <label>Select Timing</label>
          <div style={{ display: 'flex', alignItems: 'center', marginTop: '10px' }}>
            <label style={{ marginRight: '20px' }}>
              <input
                type="checkbox"
                name="is_am"
                checked={formData.is_am}
                onChange={handleInputChange}
              />
              AM
            </label>
            <label>
              <input
                type="checkbox"
                name="is_pm"
                checked={formData.is_pm}
                onChange={handleInputChange}
              />
              PM
            </label>
          </div>
          {errors.timing && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {errors.timing}
            </div>
          )}
        </div>

        {/* Request Reason */}
        <div style={{ marginBottom: '15px' }}>
          <label>Please state reason for work from home arrangement</label>
          <textarea
            name="request_reason"
            value={formData.request_reason}
            onChange={handleInputChange}
            style={{ width: '100%', padding: '8px', marginTop: '5px', minHeight: '100px' }}
            required
          />
          {errors.request_reason && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {errors.request_reason}
            </div>
          )}
        </div>

        {/* Submit Button */}
        <button 
          type="submit" 
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#007bff', 
            color: '#fff', 
            border: 'none', 
            borderRadius: '5px',
            cursor: 'pointer',
            width: '100%'
          }}
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default WFHRequestForm;