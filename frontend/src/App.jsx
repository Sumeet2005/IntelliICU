import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Layout from "./layouts/Layout";

import Dashboard from "./pages/DashboardV2";
import PatientProfile from "./pages/PatientProfile";
import Monitoring from "./pages/Monitoring";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import UserManagement from "./pages/UserManagement";
import UserProfile from "./pages/UserProfile";
import Telemetry from "./pages/Telemetry";
import HospitalAssistant from "./pages/HospitalAssistant";
import { AuthProvider } from "./context/AuthContext";
import AuthGuard from "./components/auth/AuthGuard";
import PermissionGuard from "./components/auth/PermissionGuard";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route
            element={
              <AuthGuard>
                <Layout />
              </AuthGuard>
            }
          >
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route
              path="/dashboard"
              element={
                <PermissionGuard requiredPermission="Dashboard" showFallback>
                  <Dashboard />
                </PermissionGuard>
              }
            />
            <Route
              path="/patients/:patientId"
              element={
                <PermissionGuard requiredPermission="Patients" showFallback>
                  <PatientProfile />
                </PermissionGuard>
              }
            />
            <Route
              path="/monitoring"
              element={
                <PermissionGuard requiredPermission="Patients" showFallback>
                  <Monitoring />
                </PermissionGuard>
              }
            />
            <Route
              path="/analytics"
              element={
                <PermissionGuard requiredPermission="Analytics" showFallback>
                  <Analytics />
                </PermissionGuard>
              }
            />
            <Route
              path="/settings"
              element={
                <PermissionGuard requiredPermission="Settings" showFallback>
                  <Settings />
                </PermissionGuard>
              }
            />
            <Route
              path="/users"
              element={
                <PermissionGuard requiredPermission="UserManagement" showFallback>
                  <UserManagement />
                </PermissionGuard>
              }
            />
            <Route
              path="/profile"
              element={
                <UserProfile />
              }
            />
            <Route
              path="/telemetry"
              element={
                <PermissionGuard requiredPermission="Patients" showFallback>
                  <Telemetry />
                </PermissionGuard>
              }
            />
            <Route
              path="/hospital-assistant"
              element={
                <PermissionGuard requiredPermission="ClinicalAI" showFallback>
                  <HospitalAssistant />
                </PermissionGuard>
              }
            />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
