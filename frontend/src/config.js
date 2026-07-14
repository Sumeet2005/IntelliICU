const getApiUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) return import.meta.env.VITE_API_BASE_URL;
  const hostname = typeof window !== "undefined" ? window.location.hostname : "127.0.0.1";
  return `http://${hostname}:8000/api`;
};

const getWsUrl = () => {
  if (import.meta.env.VITE_WS_BASE_URL) return import.meta.env.VITE_WS_BASE_URL;
  const hostname = typeof window !== "undefined" ? window.location.hostname : "127.0.0.1";
  return `ws://${hostname}:8000/ws`;
};

const config = {
  API_BASE_URL: getApiUrl(),
  WS_BASE_URL: getWsUrl(),
  ESCALATION_L2_SECONDS: 15,
  ESCALATION_L3_SECONDS: 30,
};

export default config;

