import React from "react";
import { Sun, Moon } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { SignedIn, SignedOut, UserButton } from "@clerk/clerk-react";

function MainNavbar({ darkMode, toggleDarkMode }) {
  const navigate = useNavigate();

  return (
    <nav className="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 transition-colors duration-200">
      <div className="container mx-auto p-4">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold font-IBM">AI Agent Workshop</h1>
          <div className="flex items-center">
            <SignedIn>
              <button
                onClick={toggleDarkMode}
                className="p-2 mr-4 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
              >
                {darkMode ? <Sun size={24} /> : <Moon size={24} />}
              </button>
              {/* <button
                onClick={() => navigate("/dashboard")}
                className="bg-sky-500 hover:bg-sky-600 text-white font-bold py-2 px-4 rounded mr-4"
              >
                Go to Dashboard
              </button> */}
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
            <SignedOut>
              <button
                onClick={toggleDarkMode}
                className="p-2 mr-4 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
              >
                {darkMode ? <Sun size={24} /> : <Moon size={24} />}
              </button>
              <button
                onClick={() => navigate("/sign-in")}
                className="bg-sky-500 hover:bg-sky-600 text-white font-bold py-2 px-4 rounded"
              >
                Sign Up / Log In
              </button>
            </SignedOut>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default MainNavbar;
