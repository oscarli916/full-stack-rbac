import HomePage from "../pages/homePage";

interface Route {
	container: () => JSX.Element;
	path: string;
	showHeader: boolean;
	title?: string;
	children?: Route[];
}

export const routes: Route[] = [
	{
		container: HomePage,
		path: "/",
		showHeader: true,
		title: "Home",
	},
];
