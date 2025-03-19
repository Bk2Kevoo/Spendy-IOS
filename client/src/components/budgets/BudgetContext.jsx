import { useState } from "react";
import toast from "react-hot-toast"
import Loader from "react-loaders"

// This has to be where my CRUD for my BUDGETS are going to be POST, PATCH, DELETE
function BudgetProvider() {

    const [budgets, setBudgets] = useState([]);
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const fetchBudgets = async () => {
        setLoading(true)
        setError(null)
        try {
            const response = await fetch("api/v1/budgets")
            if(!response.ok) {
                toast.error("Failed to Fetch api/v1/budgets")
            }
            const data = await response.json();
            setBudgets(data)
        } catch (error) {
            toast.error("Failed to fetch budgets")
        } finally {
            setLoading(false);
        }
    };

    // useEffect(() => {
    //     fetchBudgets()
    // }, [])

    const addBudget = async (newBudget) => {
        setLoading(true)
        setError(null)
        try{
            const response = await fetch("api/v1/budgets/create", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(newBudget)
            });

            if(!response.ok)
                throw new Error(`HTTP error! status: ${response.status}`)

            const createResponse = await response.json()
            setBudgets([budgets, createResponse])
            // fetchBudgets()
        } catch (error) {
            toast.error("Failed to add budget")
        } finally {
            setLoading(false);
        }
    }

    const editBudget = async (updateBudget) => {
        setLoading(true)
        setError(null)
        try{
            const response = await fetch(`api/v1/budgets/${updateBudget.id}/update`, {
                method: "PATCH",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(updateBudget)
            });

            if(!response.ok)
                throw new Error(`HTTP error! status: ${response.status}`)
            // fetchBudgets()
            const createResponse = await response.json()
            setBudgets((prev) => prev.map((budget) => budget.id === createResponse.id ? createResponse : budget
        )
    );

        } catch (error) {
            toast.error("Failed to edit the budget")
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return <Loader type="pacman"/>
    }

    if (error) {
        return <p>Error: {error.message}</p>
    }

    const deleteBudget = async () => {     
        try{
            const response = await fetch(`/api/v1/budgets`)
        }
    }

    return (
        <BudgetProvider value={{budgets, fetchBudgets, addBudget, editBudget}}>
            {/* value ={fetchBudgets, budgets, editBudgets, deleteBudgets } */}
        </BudgetProvider>
    )
}


export default BudgetProvider;