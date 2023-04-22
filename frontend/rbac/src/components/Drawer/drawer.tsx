import {
	AppBar,
	Box,
	Divider,
	Drawer,
	List,
	ListItem,
	ListItemButton,
	ListItemText,
	Toolbar,
	Typography,
} from "@mui/material";
import { routes } from "../../routes/routes";
import { useNavigate } from "react-router-dom";

interface ICustomDrawer {
	children: JSX.Element;
}

const CustomDrawer = ({ children }: ICustomDrawer) => {
	const navigate = useNavigate();

	return (
		<Box sx={{ display: "flex" }}>
			<AppBar
				position="fixed"
				sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
			>
				<Toolbar>
					<Typography variant="h6">Full Stack RBAC</Typography>
				</Toolbar>
			</AppBar>
			<Drawer
				variant="permanent"
				sx={{
					width: 240,
					flexShrink: 0,
					[`& .MuiDrawer-paper`]: {
						width: 240,
						boxSizing: "border-box",
					},
				}}
			>
				<Toolbar />
				<Box sx={{ overflow: "auto" }}>
					<List>
						{routes.map((route) => (
							<ListItem key={route.title} disablePadding>
								<ListItemButton
									onClick={() => navigate(route.path)}
								>
									<ListItemText primary={route.title} />
								</ListItemButton>
							</ListItem>
						))}
					</List>
					<Divider />
				</Box>
			</Drawer>
			<Box sx={{ flexGrow: 1 }}>{children}</Box>
		</Box>
	);
};

export default CustomDrawer;
