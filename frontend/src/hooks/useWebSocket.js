import { useEffect, useState } from "react";
import websocketService from "../services/websocketService";
import config from "../config";

export default function useWebSocket() {
  const [connected, setConnected] = useState(() => websocketService.isConnected("dashboard"));
  const [dashboardData, setDashboardData] = useState(null);
  const [patientsData, setPatientsData] = useState([]);
  const [alertsData, setAlertsData] = useState([]);

  useEffect(() => {
    const dashboardUrl = `${config.WS_BASE_URL}/dashboard`;

    const handleConnected = () => setConnected(true);
    const handleDisconnected = () => setConnected(false);

    const handleMessage = (message) => {
      if (!message || !message.type) return;
      switch (message.type) {
        case "dashboard_update":
          setConnected(true);
          setDashboardData(message.data);
          break;

        case "patients_update":
          setConnected(true);
          setPatientsData(message.data);
          break;

        case "alerts_update":
          setConnected(true);
          setAlertsData(message.data);
          break;

        default:
          break;
      }
    };

    websocketService.on("dashboard", "connected", handleConnected);
    websocketService.on("dashboard", "disconnected", handleDisconnected);
    websocketService.on("dashboard", "message", handleMessage);

    websocketService.connect("dashboard", dashboardUrl);

    return () => {
      websocketService.off("dashboard", "connected", handleConnected);
      websocketService.off("dashboard", "disconnected", handleDisconnected);
      websocketService.off("dashboard", "message", handleMessage);
    };
  }, []);

  return {
    connected,
    dashboardData,
    patientsData,
    alertsData,
    patients: patientsData,
    alerts: alertsData,
  };
}
