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
                toast.error("Failed to Fetch Budgets")
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

    const deleteBudget = async (budgetId) => {
        setLoading(true)     
        try{
            const token = getCookie("authToken");
            const csrfToken = getCookie("csrf_access_token");
            const response = await fetch(`api/v1/budgets/`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`, 
                    "Content-Type": "application/json",
                    "X-CSRF-TOKEN": csrfToken,
                },
                credentials: "include",
            })
            if(!response.ok) {
                throw new Error(` HTTP error status: ${response.statuts} `)
            }
            setBudgets((prevBudgets) => prevBudgets.filter((budget) => budget.id !== budgetId))
            toast.success("Deleted Budget Successully.")
        } catch (error) {
            toast.error('Failed to Delete Budget')
        } finally {
            setLoading(false);
        }
    }

    const getBudgetsId = async (budgetsId) => {
        try {
          const response = await fetch(`api/v1/budgets/${budgetsId}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          });
      
          if (!response.ok) {
            throw new Error(`Failed to fetch expense: ${response.statusText}`);
          }
          const budget = await response.json();
          return budget;
        } catch (error) {
          console.error("Error fetching expense by ID:", error);
          throw error;
        }
      };


    return (
        <BudgetProvider value={{budgets, fetchBudgets, addBudget, editBudget,getBudgetsId, deleteBudget}}>
            {/* value ={fetchBudgets, budgets, editBudgets, deleteBudgets } */}
        </BudgetProvider>
    )
}


export default BudgetProvider;