import { Menu } from 'antd';
import { AppstoreOutlined, AreaChartOutlined, BarsOutlined, HomeOutlined, PayCircleOutlined, SettingOutlined } from '@ant-design/icons';

function MenuList({darkTheme}) {
    return (
        <Menu theme= {darkTheme? 'dark': 'light'} mode='inline' className='menu-bar'>
            <Menu.Item key="home" icon={<HomeOutlined />}>
                Home
            </Menu.Item>
            <Menu.Item key="activity" icon={<AppstoreOutlined />}>
                Activity
            </Menu.Item>
            <Menu.SubMenu key="subtasks" icon={<BarsOutlined/>} title="Task">
                <Menu.Item key="task1">Task 1</Menu.Item>
                <Menu.Item key="task2">Task 2</Menu.Item>
                <Menu.Item key="task3">Task 3</Menu.Item>
            </Menu.SubMenu>
            <Menu.Item key="progress" icon={<AreaChartOutlined />}>
                Progress
            </Menu.Item>
            <Menu.Item key="payment" icon={<PayCircleOutlined />}>
                Payment
            </Menu.Item>
            <Menu.Item key="setting" icon={<SettingOutlined />}>
                Setting
            </Menu.Item>
        </Menu>
    );
}

export default MenuList;