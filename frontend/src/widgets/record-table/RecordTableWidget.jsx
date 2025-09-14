import React, { useEffect, useState } from "react";
import { QuestionTable } from "../../entities/record/ui/QuestionTable.jsx";
import { FileUpload } from "../../features/file-upload/FileUpload.jsx";
import { CategoryFilter } from "../../features/category-filter/CategoryFilter.jsx";
import { RatingFilter } from "../../features/rating-filter/RatingFilter.jsx";
import { categoryApi } from "../../entities/category/api/categoryApi.js"

export const RecordTableWidget = () => {
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [selectedRating, setSelectedRating] = useState("all");
  const [refreshSignal, setRefreshSignal] = useState(0);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await categoryApi.getAll();
        setCategories(res.data || []);
      } catch (err) {
        console.error("Ошибка загрузки категорий", err);
      }
    };
    fetchCategories();
  }, []);

  return (
    <div>
      <div style={{ marginBottom: 16, display: "flex", gap: 8 }}>
        <CategoryFilter
          categories={categories}
          selected={selectedCategories}
          onChange={setSelectedCategories}
        />
        <RatingFilter
          selected={selectedRating}
          onChange={setSelectedRating}
        />
        <FileUpload onUploadSuccess={() => setRefreshSignal(prev => prev + 1)}/>
      </div>
      <QuestionTable selectedCategories={selectedCategories} selectedRating={selectedRating} refreshData={refreshSignal}/>
    </div>
  );
};
