import { Box, Tab, Tabs, Toolbar, Typography } from "@mui/material";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { auth } from "../utils/auth";
import PermissionPage from "./permissionPage";
import _ from "lodash";
import UserPage from "./userPage";

interface TabPanelProps {
	children?: React.ReactNode;
	index: number;
	value: number;
}

const TabPanel = ({ children, value, index, ...other }: TabPanelProps) => (
	<div hidden={value !== index} {...other}>
		{value === index && <Box sx={{ p: 3 }}>{children}</Box>}
	</div>
);

const SettingPage = () => {
	const [value, setValue] = useState(0);

	const permissions = JSON.parse(localStorage.getItem("permissions")!);
	const location = useLocation();

	useEffect(() => {
		auth(location.pathname);
	}, [location.pathname]);

	return (
		<Box display="flex" flexDirection="column" minHeight="100vh">
			<Toolbar />
			<Box sx={{ borderBottom: 1, borderColor: "divider" }}>
				<Tabs
					value={value}
					onChange={(_, newValue) => setValue(newValue)}
				>
					{_.includes(permissions, "setting.read") && (
						<Tab label="User" />
					)}
					<Tab label="Role" />
					{_.includes(permissions, "setting.read") && (
						<Tab label="Permission" />
					)}
				</Tabs>
			</Box>
			<TabPanel value={value} index={0}>
				<UserPage />
			</TabPanel>
			<TabPanel value={value} index={1}>
				Role
			</TabPanel>
			<TabPanel value={value} index={2}>
				<PermissionPage />
			</TabPanel>
		</Box>
	);
};

export default SettingPage;
