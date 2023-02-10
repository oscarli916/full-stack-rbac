import App from "../App";

interface Route {
	container: () => JSX.Element;
	path: string;
	showHeader: boolean;
	title?: string;
	children?: Route[];
}

export const routes: Route[] = [
	{
		container: App,
		path: "/",
		showHeader: true,
		title: "Home",
	},
];
