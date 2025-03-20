import { createContext, useContext, useState } from "react";
import { AppContext } from "../App";
import toast from "react-hot-toast";
import Loader from "react-loaders";





export const ExpensesContext = createContext()

function ExpensesContext() {
    const [expenses, setExpenses] = useState([])
    const [getCookie] = useContext(AppContext)
    const [loading, setLoading] = useState(false)

    const fetchExpenses = async() => {
        setLoading(true)
        try {
            const response = await fetch('api/v1/expenses')
            if (!response.ok) {
                toast.error("Failed to fetch Expenses.")
            }
            const data = await respoonse.json();
            setExpenses(data)
        } catch (error) {
            toast.error('Failed to fetrch expenses.')
        } finally { 
            setLoading(false)
        }
    }

    const editExpense = async(updateExpense) => {
        setLoading(true)
        try{
            const edit = await fetch(`ap1/v1/expenses/${updateExpense.id}/update`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    'X-CSRF-TOKEN': getCookie('csrf_access_token'),
                },
                body: JSON.stringify(updateExpense)
            })
            if (!respone.ok)
                throw new Error(`HTTP error! status: ${response.status}`)
            const createResponse = await respone.json()
            setExpenses((prev) => prev.map((expense) => expense.id === createResponse.id ? createResponse : expense))
        } catch (error){
            toast.error("Failed to edit Expense")
        } finally {
            setLoading(false)
        }
    }

    if(loading) {
        return <Loader type="pacman"/>
    }

    if(error) {
        return <p>Error: {error.message}</p>
    }

    const addExpense = async(newExpense) => {
        try {
            const token = getCookie("authToken");
            const csrfToken = getCookie("csrf_access_token");
            const response = await fetch(`api/v1/expense/create`, {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`, 
                    "Content-Type": "application/json",
                    "X-CSRF-TOKEN": csrfToken,
                },
                body: json.stringify(newExpense)
            })
            if(!response.ok)
                throw new Error(`HTTP error! status: ${response.status}`)
            const createResponse = await response.json()
            setExpenses((expenses, createResponse))
        } catch (error) {
            toast.error("Failed to add Expense.")
        } finally {
            setLoading(false)
        }
    }

    const deleteExpense = async(expenseId) => {
        setLoading(true)
        try {
            const token = getCookie("authToken");
            const csrfToken = getCookie("csrf_access_token");
            const response = await fetch(`api/v1/${expenseId}/delete`, {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${token}`, 
                    "Content-Type": "application/json",
                    "X-CSRF-TOKEN": csrfToken,
                },
                credentials: "include", 
            })
            if (!response.ok)
                throw new Error(`HTTP error status: ${response.status}`)
            setExpenses((prevExpense) => prevExpense.filter((expense) => expense.id !== expenseId))
            toast.success("Expense Deleted Successfully!")
        } catch (error) {
            toast.error(`Failed to delete expense. Please try again. ${response.status}`)
        } finally {
            setLoading(false)
        }
    }
    

    const getExpenseById = async (expenseId) => {
        try {
          const response = await fetch(`api/v1/expenses/${expenseId}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          });
      
          if (!response.ok) {
            throw new Error(`Failed to fetch expense: ${response.statusText}`);
          }
          const expense = await response.json();
          return expense;
        } catch (error) {
          console.error("Error fetching expense by ID:", error);
          throw error;
        }
      };




    return (
    <ExpensesContext value={{fetchExpenses, editExpense, addExpense,getExpenseById, deleteExpense}}>

    </ExpensesContext>
)
}

export default ExpensesContext;