import api from "../api/axios";

let configPromise = null;
let providersPromise = null;
let modelsPromise = null;

export const aiService = {
  async analyzePatient(payload) {
    const response = await api.post("/clinical-ai/", payload);
    return response.data;
  },

  async getProviders() {
    if (!providersPromise) {
      providersPromise = api.get("/ai/providers").then(res => res.data).catch(err => {
        providersPromise = null;
        throw err;
      });
    }
    return providersPromise;
  },

  async getModels() {
    if (!modelsPromise) {
      modelsPromise = api.get("/ai/models").then(res => res.data).catch(err => {
        modelsPromise = null;
        throw err;
      });
    }
    return modelsPromise;
  },

  async getConfig() {
    if (!configPromise) {
      configPromise = api.get("/ai/config").then(res => res.data).catch(err => {
        configPromise = null;
        throw err;
      });
    }
    return configPromise;
  },

  async updateConfig(config) {
    const res = await api.put("/ai/config", config);
    // Invalidate caches on update
    configPromise = null;
    providersPromise = null;
    modelsPromise = null;
    return res.data;
  },

  async getHealth() {
    const res = await api.get("/ai/health");
    return res.data;
  },
};