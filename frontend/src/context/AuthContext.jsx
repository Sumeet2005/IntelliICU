import { createContext, useContext, useState, useEffect, useMemo } from "react";
import { authService } from "../services/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const login = async (username, password) => {
    try {
      await authService.login(username, password);
      const profile = await authService.getCurrentUser();
      setUser(profile);
      return profile;
    } catch (err) {
      setUser(null);
      throw err;
    }
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  useEffect(() => {
    const initAuth = async () => {
      if (authService.hasSession()) {
        try {
          const profile = await authService.getCurrentUser();
          setUser(profile);
        } catch (err) {
          console.error("Session restoration failed:", err);
          setUser(null);
        }
      }
      setLoading(false);
    };

    initAuth();

    const handleLogoutEvent = () => {
      setUser(null);
    };

    window.addEventListener("auth_logout", handleLogoutEvent);
    return () => {
      window.removeEventListener("auth_logout", handleLogoutEvent);
    };
  }, []);

  const value = useMemo(() => ({
    user,
    loading,
    login,
    logout,
  }), [user, loading]);

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
