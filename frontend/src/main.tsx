import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import App from "./App";
import "./index.css";

/**
 * React Query client configuration.
 *
 * Global defaults:
 * - staleTime: 0 (queries are immediately stale; each hook overrides as needed)
 * - retry: 1 (retry failed requests once before showing error)
 * - refetchOnWindowFocus: false (avoid unexpected refetches for ML endpoints)
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime:           0,
      retry:               1,
      refetchOnWindowFocus:false,
    },
  },
});

const root = document.getElementById("root");
if (!root) throw new Error("#root element not found");

createRoot(root).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      {/* Only renders in development */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </StrictMode>,
);
