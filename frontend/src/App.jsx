import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import MainNavbar from "./components/MainNavbar";

const FeatureCard = ({ title, description, icon }) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
    className="bg-none"
  >
    <Card className="h-full bg-none">
      <CardHeader>
        <div className="flex items-center space-x-2">
          {icon}
          <h3 className="text-xl font-semibold font-IBM tracking-wider">{title}</h3>
        </div>
      </CardHeader>
      <CardContent>
        <p className="tracking-wide">{description}</p>
      </CardContent>
    </Card>
  </motion.div>
);

const App = () => {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const isDarkMode = localStorage.getItem("darkMode") === "true";
    setDarkMode(isDarkMode);
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    }
  }, []);

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem("darkMode", newDarkMode);
    document.documentElement.classList.toggle("dark");
  };

  const features = [
    {
      title: "Create Custom AI Agents",
      description: "Build AI agents tailored to your specific needs and tasks.",
      icon: <span className="text-2xl">🤖</span>,
    },
    {
      title: "Advanced Training",
      description: "Train your agents using state-of-the-art machine learning models.",
      icon: <span className="text-2xl">🧠</span>,
    },
    {
      title: "Easy Deployment",
      description: "Deploy your agents seamlessly to solve real-world problems.",
      icon: <span className="text-2xl">🚀</span>,
    },
    {
      title: "Performance Monitoring",
      description: "Track and improve your agents' performance over time.",
      icon: <span className="text-2xl">📊</span>,
    },
  ];

  return (
    <div className={`${darkMode ? "dark" : ""}`} >
      <MainNavbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
      <div id="landing" className="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200 transition-colors duration-200 min-h-screen">
        <div className="container mx-auto p-4 bg-none">
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-12 text-center mt-40"
          >
            <h2 className="text-5xl font-bold mb-4 font-IBM text-sky-500">
              Welcome to AI Agent Workshop
            </h2>
            <p className="text-xl mb-16">
              Build, train, and deploy your own AI agents with our cutting-edge
              platform.
            </p>
          </motion.div>
          <div className="grid grid-cols-1 justify-items-center bg-none md:grid-cols-2 gap-4">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;