import React, { useState } from 'react';
import { ArrowRight, CheckCircle, XCircle, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react';

const ExpandableSection = ({ title, children, initiallyExpanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(initiallyExpanded);

  return (
    <div className="mb-4">
      <button
        className="flex items-center justify-between w-full p-4 bg-gray-200 dark:bg-gray-700 rounded-lg focus:outline-none"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <span className="text-lg font-semibold">{title}</span>
        {isExpanded ? <ChevronUp /> : <ChevronDown />}
      </button>
      {isExpanded && <div className="mt-2">{children}</div>}
    </div>
  );
};

const ProcessStep = ({ title, details, status }) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="text-green-500" />;
      case 'failed':
        return <XCircle className="text-red-500" />;
      case 'warning':
        return <AlertTriangle className="text-yellow-500" />;
      default:
        return null;
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md mb-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-semibold">{title}</h3>
        {getStatusIcon()}
      </div>
      <p className="text-sm text-gray-600 dark:text-gray-400">{details}</p>
    </div>
  );
};

const DecisionProcessVisualization = ({ result }) => {
  if (!result) return null;

  const { plan, results, evaluation } = result;

  return (
    <div className="bg-gray-100 dark:bg-gray-900 p-6 rounded-lg shadow-lg mb-8">
      <h2 className="text-2xl font-bold mb-6">Decision Process Visualization</h2>
      
      <ExpandableSection title="Planning Stage" initiallyExpanded={true}>
        {plan.map((step, index) => (
          <div key={index} className="flex items-start mb-4">
            <div className="flex-shrink-0 mr-4 mt-1">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">
                {index + 1}
              </div>
            </div>
            <ProcessStep
              title={step.action}
              details={step.description}
              status="completed"
            />
          </div>
        ))}
      </ExpandableSection>

      <ExpandableSection title="Execution Stage">
        {results.map((result, index) => (
          <div key={index} className="flex items-start mb-4">
            <div className="flex-shrink-0 mr-4 mt-1">
              <ArrowRight className="text-gray-500" size={24} />
            </div>
            <ProcessStep
              title={`Step ${index + 1} Execution`}
              details={`Result: ${result.result}. Time taken: ${result.time_taken} minutes.`}
              status={result.side_effects ? 'warning' : 'completed'}
            />
          </div>
        ))}
      </ExpandableSection>

      <ExpandableSection title="Evaluation Stage">
        <ProcessStep
          title="Overall Evaluation"
          details={`Score: ${evaluation.score}. ${evaluation.summary}`}
          status={evaluation.score > 80 ? 'completed' : evaluation.score > 50 ? 'warning' : 'failed'}
        />
        <div className="mt-4">
          <h4 className="font-semibold mb-2">Key Learnings:</h4>
          <ul className="list-disc list-inside">
            {evaluation.lessons.map((lesson, index) => (
              <li key={index} className="text-sm text-gray-600 dark:text-gray-400">{lesson}</li>
            ))}
          </ul>
        </div>
      </ExpandableSection>
    </div>
  );
};

export default DecisionProcessVisualization;