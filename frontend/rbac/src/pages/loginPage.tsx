import { Box } from "@mui/material";
import { useState } from "react";
import Login from "../components/Login";

const LoginPage = () => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	return (
		<Box
			alignItems="center"
			display="flex"
			justifyContent="center"
			minHeight="100vh"
		>
			<Login
				email={email}
				setEmail={setEmail}
				password={password}
				setPassword={setPassword}
			/>
		</Box>
	);
};

export default LoginPage;
