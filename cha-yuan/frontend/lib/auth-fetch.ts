/**
 * Isomorphic authentication fetch utility
 * Works in both Server Components and Client Components
 */

import { cookies } from "next/headers";

interface AuthFetchOptions extends RequestInit {
  skipAuth?: boolean;
}

interface UserProfile {
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  postal_code: string;
  has_pdpa_consent: boolean;
}

/**
 * Make authenticated API requests
 * Works in both Server and Client Components
 */
export async function authFetch(
  url: string,
  options: AuthFetchOptions = {}
): Promise<Response> {
  const { skipAuth = false, ...fetchOptions } = options;

  // Detect if we're on the server
  const isServer = typeof window === "undefined";

  if (isServer) {
    // Server-side: Use direct backend URL with cookie
    return serverFetch(url, fetchOptions, skipAuth);
  } else {
    // Client-side: Use BFF proxy
    return clientFetch(url, fetchOptions, skipAuth);
  }
}

/**
 * Server-side fetch with direct backend access
 */
async function serverFetch(
  url: string,
  options: RequestInit,
  skipAuth: boolean
): Promise<Response> {
  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
  const targetUrl = url.startsWith("http") ? url : `${backendUrl}${url}`;

  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  headers.set("Accept", "application/json");
  headers.set("X-SG-Timezone", "Asia/Singapore");
  headers.set("Accept-Language", "en-SG");

  // Get token from cookie on server
  if (!skipAuth) {
    try {
      const cookieStore = await cookies();
      const token = cookieStore.get("access_token")?.value;

      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
    } catch (error) {
      // Cookies not available (e.g., during static generation)
      console.warn("Could not access cookies:", error);
    }
  }

  return fetch(targetUrl, {
    ...options,
    headers,
  });
}

/**
 * Client-side fetch via BFF proxy
 */
async function clientFetch(
  url: string,
  options: RequestInit,
  skipAuth: boolean
): Promise<Response> {
  // Client-side: Route through BFF proxy
  const proxyUrl = `/api/proxy${url.replace("/api/v1", "")}`;

  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  headers.set("Accept", "application/json");
  headers.set("X-SG-Timezone", "Asia/Singapore");
  headers.set("Accept-Language", "en-SG");

  const response = await fetch(proxyUrl, {
    ...options,
    headers,
    credentials: "include", // Send cookies
  });

  // Handle token refresh on 401
  if (response.status === 401 && !skipAuth) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      // Retry the request
      return fetch(proxyUrl, {
        ...options,
        headers,
        credentials: "include",
      });
    }
  }

  return response;
}

/**
 * Try to refresh the access token
 */
async function tryRefreshToken(): Promise<boolean> {
  try {
    const response = await fetch("/api/proxy/auth/refresh/", {
      method: "POST",
      credentials: "include",
    });

    return response.ok;
  } catch (error) {
    console.error("Token refresh failed:", error);
    return false;
  }
}

/**
 * Check if user is authenticated
 * Client-side only
 */
export async function isAuthenticated(): Promise<boolean> {
  if (typeof window === "undefined") {
    return false; // Can't determine auth status on server
  }

  try {
    const response = await authFetch("/api/v1/auth/me", {
      method: "GET",
    });

    return response.ok;
  } catch (error) {
    return false;
  }
}

/**
 * Get current user profile
 * Returns null if not authenticated
 */
export async function getCurrentUser(): Promise<UserProfile | null> {
  try {
    const response = await authFetch("/api/v1/auth/me", {
      method: "GET",
    });

    if (response.ok) {
      return await response.json();
    }

    return null;
  } catch (error) {
    console.error("Failed to get user:", error);
    return null;
  }
}
