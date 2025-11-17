// Claude is Work to Build this Project
/**
 * API Service Client for TutorGPT Backend
 * Handles all HTTP requests to FastAPI backend
 */

const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://api.tutorgpt.com' // Replace with production URL
  : 'http://localhost:8000';

// ============================================================================
// Types
// ============================================================================

export interface SignupRequest {
  email: string;
  password: string;
  programming_experience: 'beginner' | 'intermediate' | 'advanced';
  ai_experience: 'none' | 'basic' | 'intermediate' | 'advanced';
  learning_style: 'visual' | 'practical' | 'conceptual' | 'mixed';
  preferred_language: 'en' | 'es' | 'fr' | 'de' | 'zh' | 'ja';
  full_name?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: UserProfile;
}

export interface UserProfile {
  id: number;
  email: string;
  full_name?: string;
  programming_experience: string;
  ai_experience: string;
  learning_style: string;
  preferred_language: string;
  created_at: string;
  last_login: string;
  is_active: boolean;
}

export interface PersonalizedContentResponse {
  page_path: string;
  markdown_content: string;
  generated_at: string;
  cached: boolean;
  model_version: string;
}

// ============================================================================
// API Client Class
// ============================================================================

class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Get authorization headers with JWT token
   */
  private getAuthHeaders(): HeadersInit {
    const token = this.getToken();
    if (token) {
      return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      };
    }
    return {
      'Content-Type': 'application/json',
    };
  }

  /**
   * Get JWT token from localStorage
   */
  private getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('tutorgpt_token');
  }

  /**
   * Save JWT token to localStorage
   */
  private saveToken(token: string): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('tutorgpt_token', token);
  }

  /**
   * Save user profile to localStorage
   */
  private saveUser(user: UserProfile): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem('tutorgpt_user', JSON.stringify(user));
  }

  /**
   * Get user profile from localStorage
   */
  getUser(): UserProfile | null {
    if (typeof window === 'undefined') return null;
    const userStr = localStorage.getItem('tutorgpt_user');
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * Clear auth data from localStorage
   */
  clearAuth(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('tutorgpt_token');
    localStorage.removeItem('tutorgpt_user');
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // ==========================================================================
  // Authentication Endpoints
  // ==========================================================================

  /**
   * Sign up a new user
   */
  async signup(data: SignupRequest): Promise<AuthResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Signup failed');
    }

    const authData: AuthResponse = await response.json();

    // Save token and user to localStorage
    this.saveToken(authData.access_token);
    this.saveUser(authData.user);

    return authData;
  }

  /**
   * Log in existing user
   */
  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    const authData: AuthResponse = await response.json();

    // Save token and user to localStorage
    this.saveToken(authData.access_token);
    this.saveUser(authData.user);

    return authData;
  }

  /**
   * Get current user profile (validates token)
   */
  async getCurrentUser(): Promise<UserProfile> {
    const response = await fetch(`${this.baseURL}/api/v1/auth/me`, {
      method: 'GET',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      // Token invalid or expired
      this.clearAuth();
      throw new Error('Unauthorized');
    }

    const user: UserProfile = await response.json();
    this.saveUser(user);
    return user;
  }

  /**
   * Log out user
   */
  async logout(): Promise<void> {
    this.clearAuth();
  }

  // ==========================================================================
  // Content Endpoints
  // ==========================================================================

  /**
   * Get personalized content for a page
   */
  async getPersonalizedContent(pagePath: string): Promise<PersonalizedContentResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/content/personalized/${pagePath}`, {
      method: 'GET',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired
        this.clearAuth();
        throw new Error('Session expired. Please log in again.');
      }
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch personalized content');
    }

    return await response.json();
  }

  /**
   * Get summary for a page (no auth required)
   */
  async getSummary(pagePath: string): Promise<any> {
    const response = await fetch(`${this.baseURL}/api/v1/content/summary?page_path=${encodeURIComponent(pagePath)}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch summary');
    }

    return await response.json();
  }
}

// Export singleton instance
export const apiClient = new APIClient();

// Export default for convenience
export default apiClient;
