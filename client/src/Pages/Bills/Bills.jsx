import React from 'react'
import "./Bills.css"
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';

function Bills() {
  return (
    <div className='calendar-container'>
    <div>
        <FullCalendar
            plugins={[interactionPlugin, dayGridPlugin, timeGridPlugin]}
            headerToolbar={
                {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                }
            }
            allDaySlot={false}
            initialView='dayGridMonth'
            slotDuration={"01:00:00"}
            editable={true}
            selectable={true}
            selectMirror={true}
            dayMaxEvent={true}
            weekends={true}
            nowIndicator={true}
        />
    </div>
</div>
  )
}

export default Bills
