import { Dropdown, Menu, Checkbox, Button } from "antd";
import { DownOutlined } from "@ant-design/icons";

export const CategoryFilter = ({ categories = [], selected = [], onChange }) => {
  const items = categories.map((cat) => ({
    key: cat.id ?? cat,
    label: (
      <Checkbox
        checked={selected.includes(cat.id ?? cat)}
        onChange={(e) => {
          if (e.target.checked) {
            onChange([...selected, cat.id ?? cat]);
          } else {
            onChange(selected.filter((c) => c !== (cat.id ?? cat)));
          }
        }}
      >
        {cat.name ?? cat}
      </Checkbox>
    ),
  }));

  return (
    <Dropdown menu={{ items }} trigger={["click"]}>
      <Button>
        Фильтр по категориям <DownOutlined />
      </Button>
    </Dropdown>
  );
};
