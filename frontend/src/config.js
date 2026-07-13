const config = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  WS_BASE_URL: import.meta.env.VITE_WS_BASE_URL || "ws://localhost:8000/ws",
  ESCALATION_L2_SECONDS: 15,
  ESCALATION_L3_SECONDS: 30,
};

export default config;
