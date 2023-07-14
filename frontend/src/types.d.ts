export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
}

export interface RegisterResponse {
  accessToken: string;
  userData: object;
  userAbilities: [];
}

export interface UserData {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: string;
  password: boolean;
}
