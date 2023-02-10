import React from "react";
import ReactDOM from "react-dom/client";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import {
	createBrowserRouter,
	RouteObject,
	RouterProvider,
} from "react-router-dom";
import LoginPage from "./pages/loginPage";
import ProtectedRoute from "./routes/protectedRoute";
import { routes } from "./routes/routes";

const root = ReactDOM.createRoot(
	document.getElementById("root") as HTMLElement
);

let router: RouteObject[] = [
	{
		path: "/login",
		element: <LoginPage />,
	},
];

routes.forEach((route) => {
	router.push({
		path: route.path,
		element: (
			<ProtectedRoute>
				<route.container />
			</ProtectedRoute>
		),
	});
});

root.render(
	<React.StrictMode>
		<RouterProvider router={createBrowserRouter(router)} />
		<ToastContainer />
	</React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
