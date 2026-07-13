import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { User, Lock, Mail, Shield, Briefcase, X, ShieldAlert, Key } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { userService } from "../services/userService";

export default function UserProfile() {
  const { user } = useAuth();
  const [changeOpen, setChangeOpen] = useState(false);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    if (!oldPassword.trim() || !newPassword.trim()) {
      setError("Please fill out all passcode fields.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError("New passwords do not match.");
      return;
    }
    try {
      setLoading(true);
      setError("");
      setSuccess("");
      await userService.changeMyPassword(oldPassword, newPassword);
      setSuccess("Your passcode has been updated successfully.");
      setOldPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setTimeout(() => setChangeOpen(false), 2000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update password.");
    } finally {
      setLoading(false);
    }
  };

  const openChange = () => {
    setOldPassword("");
    setNewPassword("");
    setConfirmPassword("");
    setError("");
    setSuccess("");
    setChangeOpen(true);
  };

  return (
    <div className="p-8 max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="border-b border-slate-100 pb-5">
        <h1 className="text-3xl font-black text-slate-800">My Clinical Profile</h1>
        <p className="mt-1 text-xs text-slate-500">View personal metadata and secure login credentials</p>
      </div>

      {/* Main card */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-[30px] border border-slate-200 bg-white p-8 shadow-xl relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 h-40 w-40 rounded-full bg-slate-50 blur-[50px] z-0" />
        
        <div className="relative z-10 flex flex-col sm:flex-row items-center gap-6">
          <div className="h-20 w-20 rounded-3xl bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center font-extrabold text-white text-3xl shadow-lg shadow-cyan-600/10 uppercase">
            {user ? user.username.slice(0, 2) : "ME"}
          </div>
          
          <div className="text-center sm:text-left space-y-1">
            <h2 className="text-2xl font-black text-slate-800 capitalize">{user?.username}</h2>
            <span className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-50 text-indigo-700 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide">
              <Shield size={11} />
              {user?.role}
            </span>
          </div>
        </div>

        <div className="border-t border-slate-100 mt-8 pt-6 grid grid-cols-1 md:grid-cols-2 gap-5 text-xs font-semibold text-slate-500">
          <div className="bg-slate-50/50 p-4 rounded-2xl border border-slate-100">
            <span className="text-[10px] text-slate-400 font-extrabold uppercase tracking-wider block">Email Coordinate</span>
            <div className="flex items-center gap-2 mt-1.5 font-bold text-slate-700">
              <Mail size={13} className="text-slate-500" />
              {user?.email}
            </div>
          </div>
          <div className="bg-slate-50/50 p-4 rounded-2xl border border-slate-100">
            <span className="text-[10px] text-slate-400 font-extrabold uppercase tracking-wider block">Department Assignee</span>
            <div className="flex items-center gap-2 mt-1.5 font-bold text-slate-700">
              <Briefcase size={13} className="text-slate-500" />
              {user?.department || "No Department Assigned"}
            </div>
          </div>
        </div>

        <div className="border-t border-slate-100 mt-8 pt-6 flex justify-end">
          <button
            onClick={openChange}
            className="flex items-center gap-2 rounded-2xl bg-slate-900 hover:bg-slate-850 text-white px-5 py-3.5 text-xs font-bold transition shadow-md"
          >
            <Key size={14} />
            Change My Password
          </button>
        </div>
      </motion.div>

      {/* Password change dialog */}
      <AnimatePresence>
        {changeOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" onClick={() => setChangeOpen(false)} />
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="relative w-full max-w-md rounded-3xl bg-white p-7 border border-slate-200 shadow-2xl z-10 space-y-6"
            >
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <h3 className="text-lg font-black text-slate-800 flex items-center gap-2">
                  <Lock size={18} className="text-slate-600" />
                  Change Passcode
                </h3>
                <button onClick={() => setChangeOpen(false)} className="p-1 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-lg">
                  <X size={18} />
                </button>
              </div>

              {error && (
                <div className="flex items-start gap-2.5 rounded-xl border border-red-100 bg-red-50 p-3.5 text-xs text-red-600 font-semibold">
                  <ShieldAlert size={16} className="shrink-0 mt-0.5" />
                  <span>{error}</span>
                </div>
              )}

              {success && (
                <div className="flex items-start gap-2.5 rounded-xl border border-emerald-100 bg-emerald-50 p-3.5 text-xs text-emerald-700 font-bold">
                  <span>{success}</span>
                </div>
              )}

              <form onSubmit={handlePasswordChange} className="space-y-4 text-xs font-semibold text-slate-500">
                <div className="space-y-1.5">
                  <label className="text-[10px] font-black uppercase text-slate-400 tracking-wider">Current Password</label>
                  <input
                    type="password"
                    required
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    placeholder="Enter current passcode"
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 focus:bg-white py-3 px-4 outline-none transition focus:border-slate-400 text-slate-800"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] font-black uppercase text-slate-400 tracking-wider">New Password</label>
                  <input
                    type="password"
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Minimum 6 characters"
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 focus:bg-white py-3 px-4 outline-none transition focus:border-slate-400 text-slate-800"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] font-black uppercase text-slate-400 tracking-wider">Confirm New Password</label>
                  <input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter new passcode"
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 focus:bg-white py-3 px-4 outline-none transition focus:border-slate-400 text-slate-800"
                  />
                </div>

                <div className="pt-4 border-t border-slate-100 flex gap-3">
                  <button
                    type="button"
                    onClick={() => setChangeOpen(false)}
                    className="flex-1 rounded-xl border border-slate-250 py-3.5 font-bold hover:bg-slate-50 transition"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="flex-1 rounded-xl bg-slate-900 hover:bg-slate-850 text-white font-bold py-3.5 transition flex items-center justify-center"
                  >
                    {loading ? (
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                    ) : (
                      "Save Password"
                    )}
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
