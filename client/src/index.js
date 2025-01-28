import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom";
import projectRouter from "./routes/routesindex";


const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
  <RouterProvider router={projectRouter} />
);