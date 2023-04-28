import { useCallback, useEffect, useState } from "react";
import { UserData } from "../schemas/user";
import { createUser, getUsers, removeUser, updateUser } from "../axios/user";
import {
	DataGrid,
	GridActionsCellItem,
	GridCellEditStopParams,
	GridColDef,
	GridRowParams,
	GridRowsProp,
	MuiBaseEvent,
	MuiEvent,
} from "@mui/x-data-grid";
import DeleteIcon from "@mui/icons-material/DeleteOutlined";
import _ from "lodash";
import { Box, Button, Modal, TextField, Typography } from "@mui/material";
import AddToolBar from "../components/Rbac";

const UserPage = () => {
	const [userData, setUserData] = useState<UserData[]>([]);
	const [modalOpen, setModalOpen] = useState(false);
	const [newEmail, setNewEmail] = useState("");
	const [newPassword, setNewPassword] = useState("");

	const jwt = localStorage.getItem("token");
	const permissions = JSON.parse(localStorage.getItem("permissions")!);

	const rows: GridRowsProp = userData;

	const columns: GridColDef[] = [
		{ field: "id", headerName: "ID", width: 150 },
		{
			field: "email",
			headerName: "Email",
			width: 200,
			editable: _.includes(permissions, "setting.update") ? true : false,
		},
		{
			field: "actions",
			type: "actions",
			headerName: "Delete",
			width: 150,
			getActions: (params: GridRowParams<UserData>) => [
				<GridActionsCellItem
					icon={<DeleteIcon />}
					label="Delete"
					onClick={async () => {
						await removeUser(params.id.toString(), jwt);
						await getUserData();
					}}
					color="inherit"
				/>,
			],
		},
	];

	const getUserData = useCallback(async () => {
		setUserData(await getUsers(jwt));
	}, [jwt]);

	useEffect(() => {
		getUserData();
	}, [getUserData]);

	return (
		<Box
			sx={{
				width: "100%",
			}}
		>
			{_.includes(permissions, "setting.read") && (
				<DataGrid
					rows={rows}
					columns={columns}
					initialState={{
						columns: {
							columnVisibilityModel: {
								actions: _.includes(
									permissions,
									"setting.delete"
								)
									? true
									: false,
							},
						},
					}}
					onCellEditStop={async (
						params: GridCellEditStopParams,
						event: MuiEvent<MuiBaseEvent>
					) => {
						const newValue = (
							(event as React.SyntheticEvent<HTMLElement>)
								.target as HTMLInputElement
						).value;
						if (newValue === undefined || newValue === params.value)
							return;
						await updateUser(params.id.toString(), newValue, jwt);
						await getUserData();
					}}
					slots={{
						toolbar: _.includes(permissions, "setting.create")
							? AddToolBar
							: null,
					}}
					slotProps={{
						toolbar: {
							openModal: () => setModalOpen(true),
							children: "Add User",
						},
					}}
				/>
			)}

			<Modal open={modalOpen} onClose={() => setModalOpen(false)}>
				<Box
					sx={{
						position: "absolute" as "absolute",
						top: "50%",
						left: "50%",
						transform: "translate(-50%, -50%)",
						width: 400,
						bgcolor: "background.paper",
						borderRadius: 2,
						boxShadow: 24,
						p: 4,
					}}
				>
					<Typography variant="h5" sx={{ mb: 5 }}>
						Create New User
					</Typography>
					<TextField
						label="User Email"
						margin="normal"
						variant="outlined"
						value={newEmail}
						onChange={(
							event: React.ChangeEvent<HTMLInputElement>
						) => {
							setNewEmail(event.target.value);
						}}
					/>
					<TextField
						label="User Password"
						margin="normal"
						type="password"
						variant="outlined"
						value={newPassword}
						onChange={(
							event: React.ChangeEvent<HTMLInputElement>
						) => {
							setNewPassword(event.target.value);
						}}
					/>
					<Button
						variant="contained"
						sx={{ mt: 2, ml: 5, height: 50 }}
						onClick={async () => {
							await createUser(newEmail, newPassword, jwt);
							await getUserData();
							console.log(newEmail, newPassword);
							setModalOpen(false);
						}}
					>
						Add
					</Button>
				</Box>
			</Modal>
		</Box>
	);
};

export default UserPage;
