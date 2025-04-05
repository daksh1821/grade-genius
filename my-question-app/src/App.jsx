
import React, { useEffect, useState } from 'react';

const QuizApp = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOptions, setSelectedOptions] = useState({});
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    fetch('http://localhost:8000/questions')
      .then(response => response.json())
      .then(data => setQuestions(data.questions))
      .catch(error => console.error('Error fetching questions:', error));
  }, []);

  const handleOptionSelect = (questionId, value) => {
    setSelectedOptions(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrev = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    const formattedAnswers = {};

    questions.forEach(q => {
      const answer = selectedOptions[q.id];
      if (q.type === 'multiple_choice' && typeof answer === 'number') {
        formattedAnswers[q.id] = q.options[answer]; // map index to string
      } else if (typeof answer === 'string') {
        formattedAnswers[q.id] = answer;
      }
    });

    try {
      const res = await fetch('http://localhost:8000/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: formattedAnswers })
      });

      const data = await res.json();
      console.log('Submission successful:', data);
      setSubmitted(true);
    } catch (error) {
      console.error('Submission failed:', error);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];
  const selectedValue = selectedOptions[currentQuestion?.id];

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Header */}
      <div className="h-16 flex items-center px-6 shadow-md">
        <h1 className="text-2xl font-bold">DevGenius</h1>
      </div>

      {/* Main Content */}
      <div className="flex flex-grow">
        {/* Left - Question */}
        <div className="w-1/2 p-8 flex items-center justify-center">
          <div className="max-w-lg">
            {currentQuestion ? (
              <h2 className="text-xl font-semibold mb-4">{currentQuestion.question}</h2>
            ) : (
              <p>Loading question...</p>
            )}
          </div>
        </div>

        {/* Right - Answer UI */}
        <div className="w-1/2 p-8 flex items-center justify-center">
          <div className="w-full max-w-md space-y-4">
            {currentQuestion?.type === 'multiple_choice' ? (
              currentQuestion.options.map((option, index) => (
                <div 
                  key={index}
                  className={`p-4 rounded-lg shadow cursor-pointer transition-all ${
                    selectedValue === index ? 'border-2 border-blue-500 bg-blue-50' : 'bg-gray-50 hover:bg-gray-100'
                  }`}
                  onClick={() => handleOptionSelect(currentQuestion.id, index)}
                >
                  <p>{option}</p>
                </div>
              ))
            ) : (
              <input
                type="text"
                className="w-full p-3 border border-gray-300 rounded"
                placeholder="Enter your answer"
                value={selectedValue || ''}
                onChange={e => handleOptionSelect(currentQuestion.id, e.target.value)}
              />
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="h-16 flex items-center justify-between px-6">
        <button 
          onClick={handlePrev}
          disabled={currentQuestionIndex === 0}
          className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
        >
          Previous
        </button>

        {currentQuestionIndex === questions.length - 1 ? (
          <button 
            onClick={handleSubmit}
            className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Submit
          </button>
        ) : (
          <button 
            onClick={handleNext}
            className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Next
          </button>
        )}
      </div>

      {/* After Submit */}
      {submitted && (
        <div className="p-4 text-center text-green-700 font-semibold">
          🎉 Quiz submitted successfully!
        </div>
      )}
    </div>
  );
};

export default QuizApp;
