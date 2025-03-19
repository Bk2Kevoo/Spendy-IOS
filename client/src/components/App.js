import React, { useEffect, useState, useMemo, createContext } from "react";
import Header from "./navigation/Header";
import { Outlet } from "react-router";
import ScrollToTop from "./ScrollToTop";

export const AppContext = createContext();

function App() {

  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  const fetchData = async (url, key) => {
    const apiUrl = "http://localhost:5555"
    try {
        const response = await fetch(`${apiUrl}/${url}`)
        if (!response.ok) {
          throw new Error(`Error fetching data from ${url}`);
        }
        const data = await response.json();
        setData((prevData) => ({...prevData, [key] : data,}))
      } catch (err) {
        setError(err.message);
      }
  }

  useEffect(() => {
    fetchData("/transactions", "transactions");
    fetchData("/expenses", "expenses");
    fetchData("/savings", "savings");
    fetchData("/budgets", "budgets");
}, []);

const value = useMemo(() => [data, error], [data, error]);

return (
  <AppContext.Provider value={value}>
      <div>
          <ScrollToTop />
          <Header />
          <Outlet />
      </div>
  </AppContext.Provider>
);
}

export default App;