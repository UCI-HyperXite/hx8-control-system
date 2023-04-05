import { useNavigate } from 'react-router-dom';
function HomeButton() {
    const navigate = useNavigate();

    function handleClick() {
        navigate("/panel2.tsx");
    }

    return (
        <button type="button" onClick={handleClick}>
            navBaby
        </button>
    );
}

export default HomeButton;
