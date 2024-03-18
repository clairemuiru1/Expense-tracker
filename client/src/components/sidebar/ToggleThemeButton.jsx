import { Button } from 'antd';
import { HiOutlineSun, HiOutlineMoon } from 'react-icons/hi'; // Corrected icon names

function ToggleThemeButton({ darkTheme, toggleTheme }) {
    return (
        <div className="toggle-btn">
            <Button onClick={toggleTheme}>
                {darkTheme ? <HiOutlineSun /> : <HiOutlineMoon />} {/* Corrected icon names */}
            </Button>
        </div>
    );
}

export default ToggleThemeButton;