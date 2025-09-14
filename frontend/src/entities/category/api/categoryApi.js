import axiosInstance from "../../../shared/api/axiosInstance.js"

export const categoryApi = {
  async getAll({ fields = [], order = [], limit, offset } = {}) {
    return axiosInstance.get("/category/", {
      params: { fields, order, limit, offset },
    });
  },


  async exists(name) {
    return axiosInstance.get("/category/exists", { params: { name } });
  },


  async create(data) {
    return axiosInstance.post("/category/", data);
  },


  async update(id, data) {
    return axiosInstance.put(`/category/${id}`, data);
  },


  async remove(id) {
    return axiosInstance.delete(`/category/${id}`);
  },


  async getOne(id) {
    return axiosInstance.get(`/category/${id}`);
  },
};
