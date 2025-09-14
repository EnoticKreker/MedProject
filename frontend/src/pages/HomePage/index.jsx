import React from "react";
import { RecordTableWidget } from "../../widgets/record-table/RecordTableWidget.jsx"

const HomePage = () => {
  return (
    <div style={{ padding: 20 }}>
      <h2>Таблица записей</h2>
      <RecordTableWidget />
    </div>
  );
};

export default HomePage;
