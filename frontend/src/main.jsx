import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import { ClerkProvider, SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";
import AIAgentDashboard from "./components/AIAgentDashboard";
import CustomSignIn from "./components/CustomSignIn";

// Import your publishable key
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Publishable Key");
}

const ProtectedRoute = ({ children }) => {
  return (
    <SignedIn>
      {children}
    </SignedIn>
  );
};

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Root element not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/">
    <Router>
        <Routes>
          <Route path="/" element={<App />} />
          <Route
            path="/sign-in/*"
            element={<SignedOut><CustomSignIn /></SignedOut>}
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <AIAgentDashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </ClerkProvider>
  </React.StrictMode>
);
