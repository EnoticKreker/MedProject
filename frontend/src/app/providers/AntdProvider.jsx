// src/app/providers/AntdProvider.jsx
import React from "react";
import { ConfigProvider } from "antd";

export const AntdProvider = ({ children }) => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#1677ff", // кастомный цвет темы
        },
      }}
    >
      {children}
    </ConfigProvider>
  );
};
