import React, { useState } from 'react';
import "./Bills.css";
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

function Bills() {
    const [currentEvents, setCurrentEvents] = useState([]);

    const handleDateSelect = (selectInfo) => {
        const title = prompt('Please enter a title for the bill');
        const amount = prompt('Please enter the bill amount');

        if (!title || !amount) {
            alert('Please enter title and amount.');
            return;
        }

        const newEvent = {
            title,
            amount,  // Include the amount property
            start: selectInfo.startStr,
            end: selectInfo.endStr,
            allDay: selectInfo.allDay
        };

        // Update calendar events state
        setCurrentEvents([...currentEvents, newEvent]);

        // Send POST request to the endpoint
        fetch('http://127.0.0.1:5000/bills', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bill_title: title,
                amount: amount,
                date: selectInfo.startStr // Assuming you want to use the start date of the event
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to create bill');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message); // Log the success message
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to create bill. Please try again.');
        });
    };

    const handleEventClick = (clickInfo) => {
        if (window.confirm('Are you sure you want to delete this event?')) {
            // Remove event from calendar events state
            setCurrentEvents(currentEvents.filter(event => event.id !== clickInfo.event.id));

        }
    };

    const renderEventContent = (eventInfo) => {
        return (
            <>
                <div className='title'>{eventInfo.event.title}</div>
                <div className='amount'>${eventInfo.event.extendedProps.amount}</div> {/* Include the amount */}
            </>
        );
    };

    return (
        <div className='calendar-container'>
            <div>
                <FullCalendar
                    plugins={[interactionPlugin, dayGridPlugin, timeGridPlugin]}
                    headerToolbar={{
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,timeGridWeek,timeGridDay'
                    }}
                    allDaySlot={false}
                    initialView='dayGridMonth'
                    slotDuration={"01:00:00"}
                    editable={true}
                    selectable={true}
                    selectMirror={true}
                    dayMaxEvent={true}
                    weekends={true}
                    nowIndicator={true}
                    events={currentEvents}
                    select={handleDateSelect}
                    eventClick={handleEventClick}
                    eventContent={renderEventContent} // Specify the renderEventContent function
                />
            </div>
        </div>
    );
}

export default Bills;
