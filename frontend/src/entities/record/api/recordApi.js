import axiosInstance from "../../../shared/api/axiosInstance.js"

export const recordApi = {
  async getAll(params) {
    return axiosInstance.get("/records", { params });
  },
  async updateCategory(id, category) {
    return axiosInstance.post(`/records/${id}/category`, { category });
  },
  async updateRating(id, rating) {
    return axiosInstance.post(`/records/${id}/rating`, { rating });
  },
  async uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);
    return axiosInstance.post("/records/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};
