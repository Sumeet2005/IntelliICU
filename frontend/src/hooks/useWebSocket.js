import { useEffect, useState } from "react";
import websocketService from "../services/websocketService";

export default function useWebSocket() {
  const [dashboardData, setDashboardData] = useState(null);
  const [patientsData, setPatientsData] = useState([]);
  const [alertsData, setAlertsData] = useState([]);

  useEffect(() => {
    const handleMessage = (message) => {
      switch (message.type) {
        case "dashboard_update":
          setDashboardData(message.data);
          break;

        case "patients_update":
          setPatientsData(message.data);
          break;

        case "alerts_update":
          setAlertsData(message.data);
          break;

        default:
          break;
      }
    };

    websocketService.on("dashboard", "message", handleMessage);

    return () => {
      websocketService.off("dashboard", "message", handleMessage);
    };
  }, []);

  return {
    dashboardData,
    patientsData,
    alertsData,
  };
}