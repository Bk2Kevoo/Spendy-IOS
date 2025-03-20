import About from "../about/About"
import ErrorPage from "../errorpage/Errorpage";
import { createBrowserRouter } from "react-router-dom";
import HomePage from "../home/HomePage";
import App from "../App";
import LandingPage from "../home/LandingPage";


const projectRouter = createBrowserRouter([
    {
        path:"/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                index: true,
                element: <LandingPage />

            },
            {
                path: "/about",
                element: <About />

            },
            {
                path:"/home",
                element: <HomePage />
            }
        ]
    }
])

export default projectRouter;