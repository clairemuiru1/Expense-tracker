import React, { useState, useEffect } from 'react';
import { PencilRuler, Trash } from 'lucide-react';
import './Bills.css';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

function Bills() {
    const [currentEvents, setCurrentEvents] = useState([]);

    useEffect(() => {
        fetchBills();
    }, []);

    const fetchBills = () => {
        fetch('http://127.0.0.1:5000/bills')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch bills');
            }
            return response.json();
        })
        .then(data => {
            setCurrentEvents(data.map(bill => ({
                id: bill.id,
                title: bill.title,
                amount: bill.amount,
                start: bill.date,
                end: bill.date,
                allDay: true,
                isNew: true
            })));
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to fetch bills. Please try again.');
        });
    };

    const handleDateSelect = (selectInfo) => {
        const title = prompt('Please enter a title for the bill');
        const amount = prompt('Please enter the bill amount');

        if (!title || !amount) {
            alert('Please enter title and amount.');
            return;
        }

        fetch('http://127.0.0.1:5000/bills', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bill_title: title,
                amount: amount,
                date: selectInfo.startStr
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to create bill');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            fetchBills(); // Refresh bills after creating a new one
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to create bill. Please try again.');
        });
    };

    const handleEventClick = (clickInfo) => {
        clickInfo.jsEvent.stopPropagation(); // Stop event propagation
    
        if (window.confirm('Are you sure you want to delete this bill?')) {
            fetch(`http://127.0.0.1:5000/bills/${clickInfo.event.id}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to delete bill');
                }
                return response.json();
            })
            .then(data => {
                console.log(data.message);
                fetchBills(); // Refresh bills after deleting one
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to delete bill. Please try again.');
            });
        }
    };    

    const handleEditBill = (billId) => {
        // const newTitle = prompt('Please enter a new title for the bill');
        const newAmount = prompt('Please enter the new bill amount');
    
        if (!newTitle || !newAmount) {
            alert('Please enter title and amount.');
            return;
        }
    
        fetch(`http://127.0.0.1:5000/bills/${billId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: newTitle,
                amount: newAmount // Include the new amount in the request body
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update bill');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            fetchBills(); // Refresh bills after updating one
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update bill. Please try again.');
        });
    };
    
    const renderEventContent = (eventInfo) => {
        return (
            <>
                <div className='title'>{eventInfo.event.title}</div>
                <div className='amount'>${eventInfo.event.extendedProps.amount}</div>
                <div className='action-buttons'>
                    {eventInfo.event.extendedProps.isNew && 
                        <div className='edit' onClick={() => handleEditBill(eventInfo.event.id)}>
                            <PencilRuler />
                        </div>
                    }
                    <div className='delete' onClick={() => handleEventClick(eventInfo)}>
                        <Trash />
                    </div>
                </div>
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
                    slotDuration='01:00:00'
                    editable={true}
                    selectable={true}
                    selectMirror={true}
                    dayMaxEvent={true}
                    weekends={true}
                    nowIndicator={true}
                    events={currentEvents}
                    select={handleDateSelect}
                    eventClick={handleEventClick}
                    eventContent={renderEventContent} 
                />
            </div>
        </div>
    );
}

export default Bills;
