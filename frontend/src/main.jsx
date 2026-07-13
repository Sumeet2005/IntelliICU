import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

import "./index.css";

import { ClinicalAIProvider } from "./context/ClinicalAIContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ClinicalAIProvider>
      <App />
    </ClinicalAIProvider>
  </React.StrictMode>
);