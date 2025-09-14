import axiosInstance from "../../../shared/api/axiosInstance.js"

export const questionApi = {
  async uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    return axiosInstance.post("/questions/upload/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },

  async getAll(page = 1, limit = 20, category_ids = [], agreement_filter = "all") {
    return axiosInstance.get("/questions/", {
      params: { page, limit, category_ids, agreement_filter },
      paramsSerializer: (params) => {
        const searchParams = new URLSearchParams();
        Object.keys(params).forEach((key) => {
          const value = params[key];
          if (Array.isArray(value)) {
            value.forEach((v) => searchParams.append(key, v));
          } else if (value !== undefined && value !== null) {
            searchParams.append(key, value);
          }
        });
        return searchParams.toString();
      },
    });
  },

  async getOne(id) {
    return axiosInstance.get(`/questions/${id}`);
  },


  async updateAgreement(id, agreement) {
    return axiosInstance.patch(`/questions/${id}/agreement`, {
      agreement,
    });
  },


  async assignCategories(questionId, categoryIds) {
    return axiosInstance.post(`/questions/${questionId}/categories`, {
      category_ids: categoryIds,
    });
  },
};
