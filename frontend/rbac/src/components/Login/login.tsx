import { Box, Button, Divider, TextField, Typography } from "@mui/material";

interface ILogin {
	email: string;
	setEmail: React.Dispatch<React.SetStateAction<string>>;
	password: string;
	setPassword: React.Dispatch<React.SetStateAction<string>>;
}

const Login = ({ email, setEmail, password, setPassword }: ILogin) => (
	<Box
		display="flex"
		flexDirection="column"
		justifyContent="center"
		sx={{
			backgroundColor: "#f0f0f0",
			borderRadius: 5,
			p: 5,
			width: 500,
		}}
	>
		<Typography sx={{ mb: 2 }} textAlign="center" variant="h4">
			Login
		</Typography>
		<Divider />
		<TextField
			fullWidth
			label="Email"
			sx={{ my: 3 }}
			variant="outlined"
			value={email}
			onChange={(e) => {
				setEmail(e.target.value);
			}}
		/>
		<TextField
			fullWidth
			label="Password"
			sx={{ my: 2 }}
			type="password"
			variant="outlined"
			value={password}
			onChange={(e) => {
				setPassword(e.target.value);
			}}
		/>
		<Button sx={{ mt: 3 }} variant="contained">
			Sign In
		</Button>
	</Box>
);

export default Login;
