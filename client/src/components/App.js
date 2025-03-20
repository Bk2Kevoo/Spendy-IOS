import React, { useEffect, useState, createContext, useCallback } from "react";
import Header from "./navigation/Header";
import { Outlet, useNavigate } from "react-router";
import ScrollToTop from "./ScrollToTop";
import toast from "react-hot-toast";

export const AppContext = createContext();

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
};

const fetchCurrentUser = async (getCookie, navigate) => {
  try {
    const csrfToken = getCookie("csrf_access_token");
    if (!csrfToken) return null; // Prevents fetching if no token exists

    const response = await fetch("/api/v1/current-user", {
      headers: {
        "X-CSRF-TOKEN": csrfToken,
      },
    });

    if (response.ok) return await response.json();

    // Try refreshing the token if the first request fails
    const refreshToken = getCookie("csrf_refresh_token");
    if (!refreshToken) return null;

    const refreshResponse = await fetch("/api/v1/refresh", {
      headers: {
        "X-CSRF-TOKEN": refreshToken,
      },
    });

    if (refreshResponse.ok) return await refreshResponse.json();

    return null;
  } catch (error) {
    toast.error(error.message || "An error has occurred. Try again later.");
    navigate("/register");
    return null;
  }
};

function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();

  const fetchUserData = useCallback(async () => {
    const user = await fetchCurrentUser(getCookie, navigate);
    if (user) setCurrentUser(user);
  }, [navigate]);

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);

  const updateUser = (value) => setCurrentUser(value);

  return (
    <AppContext.Provider value={{ getCookie }}>
      <Header />
      <ScrollToTop />
      <Outlet context={{ currentUser, updateUser, getCookie }} />
    </AppContext.Provider>
  );
}

export default App;
