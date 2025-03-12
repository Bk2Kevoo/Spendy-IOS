import App from "../App";
import About from "../about/About"
import ErrorPage from "../errorpage/Errorpage";
import { createBrowserRouter } from "react-router-dom";
import HomePage from "../home/HomePage";


const projectRouter = createBrowserRouter([
    {
        path:"/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                index: true,
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