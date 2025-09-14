import * as XLSX from "xlsx";
import { questionApi } from "../../entities/question/api/questionApi.js";

export const downloadExcel = async (selectedCategories = [], selectedRating = "all") => {
  try {
    const res = await questionApi.getAll(1, 10000, selectedCategories, selectedRating);
    const allQuestions = res.data.items;

    if (!allQuestions || allQuestions.length === 0) {
      alert("Нет данных для экспорта");
      return;
    }

    const keys = Object.keys(allQuestions[0]).filter(
      (k) => k !== "created_at" && k !== "updated_at"
    );

    const dataForExcel = allQuestions.map((q) => {
      const row = {};
      keys.forEach((k) => {
        if (k === "categories") {
          row[k] = q.categories?.map((c) => c.name).join(", ") || "";
        } else if (k === "agreement") {
          row[k] = q.agreement === true ? "Оценено" : q.agreement === false ? "Не оценено" : "";
        } else if (k === "question_text") {
          row[k] = q[k];
        } else {
          row[k] = q[k];
        }
      });
      return row;
    });

    const ws = XLSX.utils.json_to_sheet(dataForExcel);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Questions");

    XLSX.writeFile(wb, "questions.xlsx");

  } catch (err) {
    console.error("Ошибка при экспорте в Excel:", err);
  }
};
