const API_URL = "http://127.0.0.1:8000/api/alerts";

export const alertService = {
  async acknowledge(alertId) {
    const response = await fetch(
      `${API_URL}/acknowledge/${alertId}`,
      {
        method: "POST",
      }
    );

    return response.json();
  },

  async resolve(alertId) {
    const response = await fetch(
      `${API_URL}/resolve/${alertId}`,
      {
        method: "POST",
      }
    );

    return response.json();
  },

  async escalate(alertId) {
    const response = await fetch(
      `${API_URL}/escalate/${alertId}`,
      {
        method: "POST",
      }
    );

    return response.json();
  },
};