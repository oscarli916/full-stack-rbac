import axios from "axios";
import { toast } from "react-toastify";
import { PermissionData } from "../schemas/permission";

const RbacAxiosInstance = axios.create({
	baseURL: `${process.env.REACT_APP_BACKEND_BASE_URL}/rbac`,
	headers: { "Content-Type": "application/json" },
});

export const createPermission = async (
	value: string,
	token: string | null
): Promise<void> => {
	try {
		await RbacAxiosInstance.post(
			"/permission",
			{ name: value },
			{
				headers: {
					Authorization: `Bearer ${token}`,
				},
			}
		);
		toast.success("Permission Created");
	} catch (error) {
		if (axios.isAxiosError(error)) {
			toast.error("you are not authorized");
			console.error({ error: error.message });
		}
	}
};

export const getPermissions = async (
	token: string | null
): Promise<PermissionData[]> => {
	try {
		const res = await RbacAxiosInstance.get("/permission", {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});
		return res.data;
	} catch (error) {
		if (axios.isAxiosError(error)) {
			toast.error("you are not authorized");
			console.error({ error: error.message });
		}
		return [] as PermissionData[];
	}
};

export const updatePermission = async (
	id: string,
	value: string,
	token: string | null
): Promise<void> => {
	try {
		await RbacAxiosInstance.patch(
			`/permission/${id}`,
			{ name: value },
			{
				headers: {
					Authorization: `Bearer ${token}`,
				},
			}
		);
		toast.success("Permission name Updated");
	} catch (error) {
		if (axios.isAxiosError(error)) {
			toast.error("you are not authorized");
			console.error({ error: error.message });
		}
	}
};

export const removePermission = async (
	id: string,
	token: string | null
): Promise<void> => {
	try {
		await RbacAxiosInstance.delete(`/permission/${id}`, {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		});
		toast.success("Permission Deleted");
	} catch (error) {
		if (axios.isAxiosError(error)) {
			toast.error("you are not authorized");
			console.error({ error: error.message });
		}
	}
};
