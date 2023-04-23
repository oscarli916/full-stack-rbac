import { Button } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { GridToolbarContainer } from "@mui/x-data-grid";

interface IAddToolBar {
	openModal: () => void;
}

const AddToolBar = ({ openModal }: IAddToolBar) => (
	<GridToolbarContainer>
		<Button startIcon={<AddIcon />} onClick={openModal}>
			Add permission
		</Button>
	</GridToolbarContainer>
);

export default AddToolBar;
