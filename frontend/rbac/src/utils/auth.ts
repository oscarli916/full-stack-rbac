import _ from "lodash";
import { routes } from "../routes/routes";

export const auth = (path: string) => {
	const permissions = JSON.parse(localStorage.getItem("permissions")!);

	routes.map((route) => {
		if (route.path === path) {
			route.permissions.map((permission) => {
				if (!_.includes(permissions, permission))
					window.location.href = "/error";
			});
		}
	});
};
