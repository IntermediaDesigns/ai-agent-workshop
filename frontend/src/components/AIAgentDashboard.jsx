import React, { useState, useEffect } from "react";
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

export default function AIAgentDashboard() {
  const { user } = useUser();
  const [task, setTask] = useState("");
  const [context, setContext] = useState("");
  const [result, setResult] = useState(null);
  const [taskHistory, setTaskHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTaskHistory();
  }, [user.id]); // Fetch task history when user ID changes

  const fetchTaskHistory = async () => {
    // In a real application, you would fetch task history for the specific user
    // For now, we'll just simulate it
    const response = await fetch("/task_history");
    const data = await response.json();
    setTaskHistory(data.task_history);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("/run_task", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${await user.getToken()}`, // Include user token for authentication
        },
        body: JSON.stringify({
          task,
          context: JSON.parse(context),
          userId: user.id, // Include user ID to associate task with user
        }),
      });
      const data = await response.json();
      setResult(data);
      await fetchTaskHistory();
    } catch (error) {
      console.error("Error:", error);
    }
    setLoading(false);
  };

  const performanceData = taskHistory.map((task, index) => ({
    name: `Task ${index + 1}`,
    score: task.evaluation.score,
  }));

  return (
    <div>
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
              ? "bg-blue-300 dark:bg-blue-700 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700"
          } text-white transition-colors duration-200`}
          disabled={loading}
        >
          {loading ? "Running..." : "Run Task"}
        </button>
      </form>

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
        <h2 className="text-2xl font-bold mb-4">Performance Over Time</h2>
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
      </div>
    </div>
  );
}
