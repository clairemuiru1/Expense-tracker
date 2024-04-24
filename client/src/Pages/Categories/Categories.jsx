import React, { useState, useEffect } from "react";
import { PencilRuler } from 'lucide-react';
import "./Categories.css";

// Function to handle editing a budget
const handleEditBudget = (id, amount, fetchBudgets) => {
    const newAmount = prompt('Enter the new budget amount:', amount);

    if (newAmount !== null) {
        fetch(`http://127.0.0.1:5000/budgets/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: newAmount,
            }),
        })
        .then(response => {
            if (response.ok) {
                console.log('Budget updated successfully');
                // Refresh budgets list after updating budget
                fetchBudgets();
            } else {
                console.error('Failed to update budget');
            }
        })
        .catch(error => console.error('Error updating budget:', error));
    }
};

function Categories() {
    const [categories, setCategories] = useState([]);
    const [budgets, setBudgets] = useState([]);
    const [newBudgetAmount, setNewBudgetAmount] = useState("");
    const [newBudgetCategory, setNewBudgetCategory] = useState("");
    const [isPlaceholderVisible, setIsPlaceholderVisible] = useState(true);

    useEffect(() => {
        // Fetch categories from backend
        fetch("http://127.0.0.1:5000/categories")
            .then((response) => response.json())
            .then((data) => setCategories(data))
            .catch((error) => console.error("Error fetching categories:", error));

        // Fetch budgets from backend
        fetch("http://127.0.0.1:5000/budgets")
            .then((response) => response.json())
            .then((data) => setBudgets(data))
            .catch((error) => console.error("Error fetching budgets:", error));
    }, []);

    const lightColors = [
        "#f9d5e5",
        "#f9edd2",
        "#d2f9f2",
        "#d2d2f9",
        "#f2d2f9",
        "#d2f9d2",
    ];

    const createBudget = () => {
        // Retrieve the token from local storage
        const token = localStorage.getItem("token");

        fetch("http://127.0.0.1:5000/budgets", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                amount: newBudgetAmount,
                category: newBudgetCategory,
            }),
        })
            .then((response) => {
                if (response.ok) {
                    console.log("Budget created successfully");
                    // Refresh budgets list after creating budget
                    fetchBudgets();
                } else {
                    console.error("Failed to create budget");
                }
            })
            .catch((error) => console.error("Error creating budget:", error));
    };

    const deleteBudget = (id) => {
        fetch(`http://127.0.0.1:5000/budgets/${id}`, {
            method: "DELETE",
        })
            .then((response) => {
                if (response.ok) {
                    console.log("Budget deleted successfully");
                    // Refresh budgets list after deleting budget
                    fetchBudgets();
                } else {
                    console.error("Failed to delete budget");
                }
            })
            .catch((error) => console.error("Error deleting budget:", error));
    };

    const fetchBudgets = () => {
        fetch("http://127.0.0.1:5000/budgets")
            .then((response) => response.json())
            .then((data) => setBudgets(data))
            .catch((error) => console.error("Error fetching budgets:", error));
    };

    const handleInputChange = (e) => {
        setNewBudgetAmount(e.target.value);
        setIsPlaceholderVisible(e.target.value === "");
    };

    const handleEnterKeyPress = (e) => {
        if (e.key === "Enter") {
            setIsPlaceholderVisible(true);
        }
    };

    return (
        <div className="categories-container">
            <hr />
            <h2>Categories</h2>
            <div className="inputs">
                <input
                    type="text"
                    placeholder={isPlaceholderVisible ? "New Budget Amount" : ""}
                    value={newBudgetAmount}
                    onChange={handleInputChange}
                    onKeyDown={handleEnterKeyPress}
                />
                <input
                    type="text"
                    placeholder="Category"
                    value={newBudgetCategory}
                    onChange={(e) => setNewBudgetCategory(e.target.value)}
                />
                <button onClick={createBudget}>Create Budget</button>
            </div>
            <ul className="category-list">
                {categories.map((category, index) => {
                    const categoryBudget = budgets.find(
                        (budget) => budget.category.name === category.name
                    );
                    return (
                        <li
                            key={category.id}
                            style={{
                                backgroundColor: lightColors[index % lightColors.length],
                            }}
                        >
                            <h3>{category.name}</h3>
                            {categoryBudget && (
                                <p>Budget Amount: $ {categoryBudget.amount}</p>
                            )}
                            {categoryBudget && (
                                <div className="action-container">
                                    <div className='edit' onClick={() => handleEditBudget(categoryBudget.id, categoryBudget.amount, fetchBudgets)}><PencilRuler /></div>
                                    <button onClick={() => deleteBudget(categoryBudget.id)}>Delete Budget</button>
                                </div>
                            )}
                        </li>
                    );
                })}
            </ul>
        </div>
    );
}

export default Categories;
