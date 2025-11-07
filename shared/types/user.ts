export interface User {
  userId: string;
  email: string;
  passwordHash: string;
  profile: UserProfile;
  createdAt: Date;
  lastLoginAt: Date;
}

export interface UserProfile {
  firstName: string;
  lastName: string;
  location?: string;
  interests?: string[];
  experience?: string;
}

export interface CreateUserRequest {
  email: string;
  password: string;
  profile: Omit<UserProfile, 'userId'>;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: Omit<User, 'passwordHash'>;
  token: string;
}