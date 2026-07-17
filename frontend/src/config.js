const hostname =
  typeof window !== "undefined"
    ? window.location.hostname
    : "localhost";

const protocol =
  typeof window !== "undefined"
    ? window.location.protocol
    : "http:";

const wsProtocol =
  protocol === "https:" ? "wss:" : "ws:";

const config = {
  API_BASE_URL:
    import.meta.env.VITE_API_BASE_URL ||
    `${protocol}//${hostname}:8000/api`,

  WS_BASE_URL:
    import.meta.env.VITE_WS_BASE_URL ||
    `${wsProtocol}//${hostname}:8000/ws`,

  ESCALATION_L2_SECONDS: 15,

  ESCALATION_L3_SECONDS: 30,
};

export default config;