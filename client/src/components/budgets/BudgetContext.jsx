import { useState } from "react";
import toast from "react-hot-toast"



// This has to be where my CRUD for my BUDGETS are going to be POST, PATCH, DELETE


function BudgetProvider() {

    const [budgets, setBudgets] = useState([])


    const fetchBudgets = async () => {
        try {
            const response = await fetch("api/v1/budgets")
            if(!response.ok) {
                toast.error("Failed to Fetch api/v1/budgets")
            }
            const data = await response.json();
            setBudgets(data)
        } catch (error) {
            toast.error("Failed to fetch budgets")
        }
    };

    const addBudget = async (newBudget) => {
        try{
            const response = await fetch("api/v1/budgets/create", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(newBudget)
            });
            const createResponse = await response.json()
            setBudgets([budgets, createResponse])
        } catch (error) {
            toast.error("Failed to add budget")
        }
    }

    const editBudget = async (updateBudget) => {
        try{
            const response = await fetch(`api/v1/budgets/${updateBudget.id}/update`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(updateBudget)
            });
            const createResponse = await response.json()
            setBudgets()
        } catch (error) {
            toast.error("Failed to edit the budget")
        }
    }



    return (
        <BudgetProvider value={{budgets, fetchBudgets, addBudget}}>
            {/* value ={fetchBudgets, budgets, editBudgets, deleteBudgets } */}
        </BudgetProvider>
    )
}


export default BudgetProvider;