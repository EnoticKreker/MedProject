import { useEffect, useState } from "react";
import { Table, Select, Radio, message, Modal, Button } from "antd";
import { questionApi } from "../../question/api/questionApi.js";
import { categoryApi } from "../../category/api/categoryApi.js";
import { downloadExcel  } from "../../../features/downloadExcel/downloadExcel.js"


const { Option } = Select;

export const QuestionTable = ({ selectedCategories = [], selectedRating = "all", refreshData }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 20;


  const fetchQuestions = async (page = 1) => {
    setLoading(true);
    try {
      const res = await questionApi.getAll(
        page,
        pageSize,
        selectedCategories,
        selectedRating
      );
      setQuestions(res.data.items || []);
      setTotal(res.data.total || 0);
      setCurrentPage(page);
    } catch {
      message.error("Ошибка загрузки вопросов");
    } finally {
      setLoading(false);
    }
  };

  // Получение категорий
  const fetchCategories = async () => {
    try {
      const res = await categoryApi.getAll();
      setCategories(res.data || []);
    } catch {
      message.error("Ошибка загрузки категорий");
    }
  };

  useEffect(() => {
    fetchQuestions(1);
    fetchCategories();
  }, [selectedCategories, selectedRating]);

    useEffect(() => {
    if (refreshData) {
      fetchQuestions(1);
      fetchCategories();
    }
  }, [refreshData]);

  const handlePageChange = (page) => {
    fetchQuestions(page);
  };

  // Динамические колонки
  const generateColumns = (data) => {
    if (!data || data.length === 0) return [];

    const keys = Object.keys(data[0]);

    const dynamicCols = keys
      .filter(
        (k) =>
          k !== "categories" &&
          k !== "agreement" &&
          k !== "created_at" &&
          k !== "updated_at"
      )
      .map((k) => {
        if (k === "question_text") {
          return {
            title: k.charAt(0).toUpperCase() + k.slice(1),
            dataIndex: k,
            key: k,
            render: (text) =>
              text && text.length > 50 ? text.slice(0, 20) + "..." : text,
          };
        } else {
          return {
            title: k.charAt(0).toUpperCase() + k.slice(1),
            dataIndex: k,
            key: k,
          };
        }
      });

    dynamicCols.push({
      title: "Категории",
      key: "categories",
      render: (_, record) => (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
          <Select
            value={record.categories?.[0]?.id}
            style={{ width: 160 }}
            onChange={(value) =>
              questionApi.assignCategories(record.question_id, [value]).then(() => fetchQuestions(currentPage))
            }
          >
            {categories.map((cat) => (
              <Option key={cat.id} value={cat.id}>
                {cat.name}
              </Option>
            ))}
          </Select>
          <div>
            {record.categories?.length
              ? record.categories.map((cat) => cat.name).join(", ")
              : "—"}
          </div>
        </div>
      ),
    });

    dynamicCols.push({
      title: "Оценка",
      key: "agreement",
      render: (_, record) => (
        <Radio.Group
          value={
            record.agreement === true
              ? "true"
              : record.agreement === false
              ? "false"
              : null
          }
          onChange={(e) =>
            questionApi
              .updateAgreement(record.question_id, e.target.value)
              .then(() => fetchQuestions(currentPage))
          }
        >
          <Radio value="true">Согласен</Radio>
          <Radio value="false">Не согласен</Radio>
        </Radio.Group>
      ),
    });

    return dynamicCols;
  };

  const handleRowClick = (record) => {
    setSelectedRecord(record);
    setIsModalVisible(true);
  }

  // Фильтрация вопросов по выбранным категориям
  const filteredQuestions = questions.filter((q) => {
    if (selectedCategories.length === 0) return true; // ничего не выбрано → показываем всё
    return q.categories?.some((cat) =>
      selectedCategories.includes(cat.id) // оставляем вопросы, у которых есть хоть одна выбранная категория
    );
  });

  return (
    <>
      <Button onClick={() => downloadExcel(selectedCategories, selectedRating)}>
        Скачать Excel
      </Button>
      <Table
        rowKey="id"
        dataSource={filteredQuestions}
        columns={generateColumns(questions)}
        loading={loading}
        pagination={{
          current: currentPage,
          pageSize,
          total,
          onChange: handlePageChange,
          showSizeChanger: false,  // отключаем выбор размера страницы
          showQuickJumper: true,   // возможность прыгнуть на любую страницу
        }}
        onRow={(record) => ({
            onClick: (event) => {
              if (event.target.closest('button, input, .ant-radio, .ant-select, .ant-select-selector, .ant-select-item')) return
              handleRowClick(record)
            }
        })}
      />

      <Modal
          title="Детали вопроса"
          open={isModalVisible}
          onCancel={() => setIsModalVisible(false)}
          footer={null}
          width={700}
        >
          {selectedRecord &&
            Object.entries(selectedRecord).map(([key, value]) => (
              <p key={key}>
                <b>{key}:</b>{" "}
                {
                  key === "categories"
                  ? value.map((cat) => cat.name).join(", ")
                  : String(value)
                }
              </p>
            ))}
      </Modal>
    </>
  );
};
