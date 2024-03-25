import React from 'react';
import "./Benefits.css";

function Benefits() {
    return (
        <div className='container'>
            <h3 className='title'>Empower Your Finances: Smart Budgeting Made Simple</h3>
            <div className='grid'>
                <div className="column">
                    <h2>Bills Scheduler</h2>
                    <p>Utilize the calendar feature to schedule and track bill payment dates
                        <br />
                        <br />
                        ensuring timely payments and effective budget management.</p>
                </div>
                <div className="column">
                    <h2>Expense Organizer</h2>
                    <p>Organize your payments by categorizing different expenses <br /><br /> helping you manage and track your financial obligations more effectively.</p>
                </div>
                <div className="column">
                    <h2>Savings Tracker</h2>
                    <p>Easily set and monitor savings goals to achieve financial milestones<br/> <br/>ensuring progress towards your desired objectives.</p>
                </div>
            </div>
        </div>
    );
}

export default Benefits;
