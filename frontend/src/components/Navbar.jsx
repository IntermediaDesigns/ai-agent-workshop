import React from "react";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  return (
    <nav className="flex items-center justify-between p-4 w-full bg-white dark:bg-gray-900 dark:text-white">
      <h1 className="text-3xl font-IBM font-bold mx-6">AI Agent Workshop</h1>
      <button
        onClick={() => navigate("/")}
        className="border-red-500 border-2 mr-6 rounded-xl py-2 px-4 hover:text-sky-500 hover:transform hover:scale-105 hover:border-red-700 dark:text-sky-400 dark:hover:text-sky-300"
      >
        Cancel
      </button>
    </nav>
  );
}

export default Navbar;
