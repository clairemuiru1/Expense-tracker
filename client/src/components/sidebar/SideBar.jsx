import React, { useState } from "react";
import { Button, Layout } from "antd";
import Logo from "./Logo";
import MenuList from "./MenuList";
import ToggleThemeButton from "./ToggleThemeButton";
import { MenuFoldOutlined, MenuUnfoldOutlined } from "@ant-design/icons";

const { Header, Sider } = Layout;

function SideBar() {
  const [darkTheme, setDarkTheme] = useState(true);
  const [collapsed, setCollapsed] = useState(false);

  const toggleTheme = () => {
    setDarkTheme(!darkTheme);
  };

  return (
    <Layout>
      <Sider
        collapsed={collapsed}
        collapsible
        trigger={null}
        theme={darkTheme ? "dark" : "light"}
        className="sidebar"
      >
        <Logo />
        <MenuList darkTheme={darkTheme} />
        <ToggleThemeButton darkTheme={darkTheme} toggleTheme={toggleTheme} />
      </Sider>
      <Layout>
        <Header style={{ background: "#fff", padding: 0 }}>
          <Button
            type="text"
            className="toggle"
            onClick={() => setCollapsed(!collapsed)}
            icon={collapsed ? <MenuFoldOutlined /> : <MenuUnfoldOutlined />}
          />
        </Header>
      </Layout>
    </Layout>
  );
}

export default SideBar;