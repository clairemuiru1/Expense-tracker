import React, { useState, useEffect } from 'react';
import "./Payments.css";

function Payments() {
  const [newTransaction, setNewTransaction] = useState({
    amount: '',
    description: '',
    category: ''
  });
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetchTransactions();
  }, []); // Fetch transactions on component mount

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewTransaction(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    fetch('http://127.0.0.1:5000/transactions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount: newTransaction.amount,
        description: newTransaction.description,
        category: newTransaction.category
      }),
    })
      .then(response => {
        if (response.ok) {
          console.log('Transaction created successfully');
          // Refresh transactions data after creating a new transaction
          fetchTransactions();
        } else {
          console.error('Failed to create transaction');
        }
      })
      .catch(error => console.error('Error creating transaction:', error));
  };

  const fetchTransactions = () => {
    fetch('http://127.0.0.1:5000/transactions')
      .then(response => response.json())
      .then(data => setTransactions(data))
      .catch(error => console.error('Error fetching transactions:', error));
  };

  return (
    <div>
      <h2>Create Transaction</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Amount:
          <input type="text" name="amount" value={newTransaction.amount} onChange={handleChange} />
        </label>
        <label>
          Description:
          <input type="text" name="description" value={newTransaction.description} onChange={handleChange} />
        </label>
        <label>
          Category:
          <input type="text" name="category" value={newTransaction.category} onChange={handleChange} />
        </label>
        <button type="submit">Create Transaction</button>
      </form>

      <div>
        <h2>Payments</h2>
        <table className="transaction-table">
          <thead>
            <tr>
              <th>Amount</th>
              <th>Description</th>
              <th>Date</th>
              <th>Category</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map(transaction => (
              <tr key={transaction.id}>
                <td>${transaction.amount}</td>
                <td>{transaction.description}</td>
                <td>{transaction.date}</td>
                <td>{transaction.category.name}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Payments;
