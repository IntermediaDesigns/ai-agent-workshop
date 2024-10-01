import { useState, useEffect } from "react";
import { useUser } from "@clerk/clerk-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import DecisionProcessVisualization from "./DecisionProcessVisualization";
import MainNavbar from "./MainNavbar";

export default function AIAgentDashboard() {
  const { user } = useUser();
  const [task, setTask] = useState("");
  const [context, setContext] = useState("");
  const [result, setResult] = useState(null);
  const [taskHistory, setTaskHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const API_URL = "http://localhost:8000"; // Update this to your backend URL

  useEffect(() => {
    fetchTaskHistory();
    const isDarkMode = localStorage.getItem("darkMode") === "true";
    setDarkMode(isDarkMode);
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    }
  }, [user.id]);

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode);
    document.documentElement.classList.toggle("dark");
  };

  const fetchTaskHistory = async () => {
    setError(null);
    try {
      const response = await fetch(`${API_URL}/task_history`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setTaskHistory(data.task_history);
    } catch (e) {
      console.error("Error fetching task history:", e);
      setError("Failed to fetch task history. Please try again later.");
      setTaskHistory([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      let token = "";
      if (user && typeof user.getToken === "function") {
        token = await user.getToken();
      }

      const response = await fetch(`${API_URL}/run_task`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token && { Authorization: `Bearer ${token}` }),
        },
        body: JSON.stringify({
          task,
          context: JSON.parse(context),
          userId: user?.id || "anonymous",
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setResult(data);
      await fetchTaskHistory();
    } catch (error) {
      console.error("Error:", error);
      setError("Failed to run task. Please check your input and try again.");
    }
    setLoading(false);
  };

  const performanceData = taskHistory.map((task, index) => ({
    name: `Task ${index + 1}`,
    score: task.evaluation.score,
  }));

  return (
    <div
      className={`min-h-screen bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 transition-colors duration-200 ${
        darkMode ? "dark" : ""
      }`}
    >
      <MainNavbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      <div className="container mx-auto p-4 bg-none">
        <form
          onSubmit={handleSubmit}
          className="mb-8 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md"
        >
          <div className="mb-4">
            <label htmlFor="task" className="block mb-2 font-semibold">
              Task:
            </label>
            <input
              type="text"
              id="task"
              value={task}
              onChange={(e) => setTask(e.target.value)}
              className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
          </div>
          <div className="mb-4">
            <label htmlFor="context" className="block mb-2 font-semibold">
              Context (JSON):
            </label>
            <textarea
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              rows="4"
            />
          </div>
          <button
            type="submit"
            className={`w-full py-2 px-4 rounded font-bold ${
              loading
                ? "bg-sky-300 dark:bg-sky-700 cursor-not-allowed"
                : "bg-sky-500 hover:bg-sky-600 dark:bg-sky-600 dark:hover:bg-sky-700"
            } text-white transition-colors duration-200`}
            disabled={loading}
          >
            {loading ? "Running..." : "Run Task"}
          </button>
        </form>

        {error && (
          <div
            className="mb-8 bg-red-100 dark:bg-red-900 border border-red-400 dark:border-red-700 text-red-700 dark:text-red-200 px-4 py-3 rounded relative"
            role="alert"
          >
            <strong className="font-bold bg-none">Error: </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {result && (
          <>
            <DecisionProcessVisualization result={result} />
            <div className="mb-8 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4">Raw Result:</h2>
              <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded overflow-x-auto">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          </>
        )}

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4 bg-none">
            Performance Over Time
          </h2>
          {taskHistory.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#8884d8"
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-600 bg-white dark:bg-gray-800 dark:text-gray-400">
              No task history available.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
