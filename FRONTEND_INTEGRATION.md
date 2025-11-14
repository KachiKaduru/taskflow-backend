# Frontend Integration Guide

This guide shows how to connect your Next.js TypeScript frontend to the Taskflow backend API deployed on Render.

## Backend API Base URL

```
https://taskflow-backend-vmm3.onrender.com
```

## Authentication Flow

1. **Register User**: `POST /auth/create-user`
2. **Login**: `POST /auth/token` → Returns `{access_token, token_type: "bearer"}`
3. **Get Current User**: `GET /users/me` (requires token)
4. **Use Token**: Include `Authorization: Bearer <token>` header in all protected requests

---

## Step 1: Environment Configuration

Create or update `.env.local` in your frontend project:

```env
NEXT_PUBLIC_API_URL=https://taskflow-backend-vmm3.onrender.com
```

---

## Step 2: API Configuration

Create `lib/api/config.ts`:

```typescript
export const API_CONFIG = {
  baseURL: process.env.NEXT_PUBLIC_API_URL || "https://taskflow-backend-vmm3.onrender.com",
  endpoints: {
    auth: {
      login: "/auth/token",
      register: "/auth/create-user",
      me: "/users/me",
    },
    tasks: "/tasks",
    events: "/events",
    appointments: "/appointments",
  },
} as const;
```

---

## Step 3: Token Storage Utility

Create `lib/auth/token.ts`:

```typescript
const TOKEN_KEY = "taskflow_access_token";

export const tokenStorage = {
  get: (): string | null => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(TOKEN_KEY);
  },

  set: (token: string): void => {
    if (typeof window === "undefined") return;
    localStorage.setItem(TOKEN_KEY, token);
  },

  remove: (): void => {
    if (typeof window === "undefined") return;
    localStorage.removeItem(TOKEN_KEY);
  },
};
```

---

## Step 4: API Client with Authentication

Create `lib/api/client.ts`:

```typescript
import { API_CONFIG } from "./config";
import { tokenStorage } from "../auth/token";

class ApiClient {
  private baseURL: string;

  constructor() {
    this.baseURL = API_CONFIG.baseURL;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = tokenStorage.get();

    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...options.headers,
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({
          detail: response.statusText,
        }));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return null as T;
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error("An unexpected error occurred");
    }
  }

  // Auth methods
  async login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append("username", email); // OAuth2PasswordRequestForm uses 'username'
    formData.append("password", password);

    const response = await this.request<{ access_token: string; token_type: string }>(
      API_CONFIG.endpoints.auth.login,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
      }
    );

    if (response.access_token) {
      tokenStorage.set(response.access_token);
    }

    return response;
  }

  async register(data: { name: string; email: string; password: string; image?: string }) {
    return this.request(API_CONFIG.endpoints.auth.register, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getCurrentUser() {
    return this.request<{ id: string; name: string; email: string }>(API_CONFIG.endpoints.auth.me);
  }

  logout() {
    tokenStorage.remove();
  }

  // Tasks
  async getTasks() {
    return this.request(`${API_CONFIG.endpoints.tasks}/all`);
  }

  async getTask(id: string) {
    return this.request(`${API_CONFIG.endpoints.tasks}/${id}`);
  }

  async createTask(data: any) {
    return this.request(`${API_CONFIG.endpoints.tasks}/create`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateTask(id: string, data: any) {
    return this.request(`${API_CONFIG.endpoints.tasks}/update/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteTask(id: string) {
    return this.request(`${API_CONFIG.endpoints.tasks}/delete/${id}`, {
      method: "DELETE",
    });
  }

  // Events
  async getEvents() {
    return this.request(`${API_CONFIG.endpoints.events}/all`);
  }

  async getEvent(id: string) {
    return this.request(`${API_CONFIG.endpoints.events}/${id}`);
  }

  async createEvent(data: any) {
    return this.request(`${API_CONFIG.endpoints.events}/create`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateEvent(id: string, data: any) {
    return this.request(`${API_CONFIG.endpoints.events}/update/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteEvent(id: string) {
    return this.request(`${API_CONFIG.endpoints.events}/delete/${id}`, {
      method: "DELETE",
    });
  }

  // Appointments
  async getAppointments() {
    return this.request(`${API_CONFIG.endpoints.appointments}/all`);
  }

  async getAppointment(id: string) {
    return this.request(`${API_CONFIG.endpoints.appointments}/${id}`);
  }

  async createAppointment(data: any) {
    return this.request(`${API_CONFIG.endpoints.appointments}/create`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateAppointment(id: string, data: any) {
    return this.request(`${API_CONFIG.endpoints.appointments}/update/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async deleteAppointment(id: string) {
    return this.request(`${API_CONFIG.endpoints.appointments}/delete/${id}`, {
      method: "DELETE",
    });
  }
}

export const apiClient = new ApiClient();
```

---

## Step 5: React Query Setup (Recommended)

If you're using React Query (TanStack Query), create `lib/api/queries.ts`:

```typescript
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "./client";
import { tokenStorage } from "../auth/token";

// Auth queries
export const useLogin = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      apiClient.login(email, password),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user"] });
    },
  });
};

export const useRegister = () => {
  return useMutation({
    mutationFn: (data: { name: string; email: string; password: string; image?: string }) =>
      apiClient.register(data),
  });
};

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ["user"],
    queryFn: () => apiClient.getCurrentUser(),
    enabled: !!tokenStorage.get(), // Only fetch if token exists
    retry: false,
  });
};

// Tasks queries
export const useTasks = () => {
  return useQuery({
    queryKey: ["tasks"],
    queryFn: () => apiClient.getTasks(),
  });
};

export const useCreateTask = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: any) => apiClient.createTask(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
  });
};

// Similar patterns for events and appointments...
```

---

## Step 6: Usage in Components

### Login Component Example

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api/client";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      await apiClient.login(email, password);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit">Login</button>
    </form>
  );
}
```

### Fetching Tasks Example

```typescript
"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api/client";
import type { TaskItem } from "@/app/_types";

export default function TasksList() {
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await apiClient.getTasks();
        setTasks(data);
      } catch (error) {
        console.error("Failed to fetch tasks:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {tasks.map((task) => (
        <div key={task.id}>
          <h3>{task.title}</h3>
          <p>{task.description}</p>
        </div>
      ))}
    </div>
  );
}
```

---

## Step 7: Protected Route Middleware

Create `middleware.ts` in your Next.js app root:

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("taskflow_access_token")?.value;
  const { pathname } = request.nextUrl;

  // Protected routes
  const protectedRoutes = ["/dashboard", "/tasks", "/events", "/appointments"];
  const isProtectedRoute = protectedRoutes.some((route) => pathname.startsWith(route));

  // Auth routes
  const authRoutes = ["/login", "/register"];
  const isAuthRoute = authRoutes.some((route) => pathname.startsWith(route));

  // Redirect to login if accessing protected route without token
  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Redirect to dashboard if accessing auth routes with token
  if (isAuthRoute && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

## Step 8: CORS Configuration (Backend)

Make sure your backend allows requests from your frontend. Update `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-frontend-domain.vercel.app",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers...
```

---

## Testing the Integration

### 1. Test Registration

```bash
curl -X POST "https://taskflow-backend-vmm3.onrender.com/auth/create-user" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 2. Test Login

```bash
curl -X POST "https://taskflow-backend-vmm3.onrender.com/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword123"
```

### 3. Test Protected Endpoint

```bash
curl -X GET "https://taskflow-backend-vmm3.onrender.com/tasks/all" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Important Notes

1. **Token Expiration**: Tokens expire after 24 hours. Implement token refresh or re-login flow.

2. **Error Handling**: Always handle 401 (Unauthorized) errors and redirect to login.

3. **CORS**: Ensure your backend CORS settings allow your frontend domain.

4. **Environment Variables**: Never commit `.env.local` to version control.

5. **Type Safety**: Use your TypeScript types from `app/_types` for all API responses.

---

## Quick Start Checklist

- [ ] Add `NEXT_PUBLIC_API_URL` to `.env.local`
- [ ] Create API configuration file
- [ ] Create token storage utility
- [ ] Create API client with authentication
- [ ] Set up React Query (optional but recommended)
- [ ] Create login/register components
- [ ] Test authentication flow
- [ ] Add protected route middleware
- [ ] Configure CORS on backend
- [ ] Test all API endpoints

---

## Need Help?

If you encounter issues:

1. Check browser console for errors
2. Verify API URL is correct
3. Check network tab for request/response details
4. Ensure token is being stored and sent correctly
5. Verify CORS settings on backend
