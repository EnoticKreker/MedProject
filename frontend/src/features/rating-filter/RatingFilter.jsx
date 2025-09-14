import { Select } from "antd";

export const RatingFilter = ({ value, onChange }) => {
  return (
    <Select
      value={value}   // теперь берем текущее значение из пропсов
      onChange={onChange}
      style={{ width: 150 }}
    >
      <Select.Option value="all">Все</Select.Option>
      <Select.Option value="true">Оцененные</Select.Option>
      <Select.Option value="false">Не оцененные</Select.Option>
    </Select>
  );
};
