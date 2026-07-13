import api from "../api/axios";

export const aiService = {
  async analyzePatient(payload) {
    const response = await api.post("/clinical-ai/", payload);
    return response.data;
  },
};