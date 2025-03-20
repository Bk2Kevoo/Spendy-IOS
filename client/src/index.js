import { createRoot } from 'react-dom/client'
import './index.css'
import { RouterProvider } from 'react-router-dom'
import projectRouter from './components/routes/routesindex';

const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
  <RouterProvider router={projectRouter}/>
)