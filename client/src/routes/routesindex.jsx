import App from "../components/App";
import About from "../components/about/About"
import ErrorPage from "../components/errorpage/Errorpage";

const projectRouter = createBrowserRouter([
    {
        path:"/",
        element: <App />,
        errorElemnt: <ErrorPage />,
        children: [
            {
                index: true,
                path:"/about",
                element: <About />

            }
        ]
    }
])

export default projectRouter;