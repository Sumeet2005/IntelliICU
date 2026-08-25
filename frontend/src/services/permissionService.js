import api from "../api/axios";

let rolesPromise = null;
let permissionsPromise = null;

export const permissionService = {
  getMyPermissions: async () => {
    const response = await api.get("/rbac/users/me/permissions");
    return response.data; // returns { role: "Doctor", permissions: ["Dashboard", "Patients", ...] }
  },

  getAllRoles: async () => {
    if (!rolesPromise) {
      rolesPromise = api.get("/rbac/roles").then(response => response.data).catch(err => {
        rolesPromise = null;
        throw err;
      });
    }
    return rolesPromise;
  },

  getAllPermissions: async () => {
    if (!permissionsPromise) {
      permissionsPromise = api.get("/rbac/permissions").then(response => response.data).catch(err => {
        permissionsPromise = null;
        throw err;
      });
    }
    return permissionsPromise;
  }
};
