import React, { useState } from 'react';
import CodeInput from './components/CodeInput';
import ReviewTabs from './components/ReviewTabs';
import Loader from './components/Loader';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

function App() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(''); // NEW: error state

  const handleSubmit = async () => {
    setLoading(true);
    setResponse(null);
    setError(''); // Reset any previous error

    try {
      const res = await fetch('http://localhost:5000/api/review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language })
      });

      const data = await res.json();

      if (res.ok) {
        setResponse(data);
      } else {
        // Handle error from backend
        setError(data.error || 'Something went wrong. Please try again.');
      }
    } catch (err) {
      console.error('API Error:', err);
      setError('Server is busy. Please try again after some time.');
    }

    setLoading(false);
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4 text-center">AI Code Review Assistant</h2>
      <CodeInput
        code={code}
        setCode={setCode}
        language={language}
        setLanguage={setLanguage}
        onSubmit={handleSubmit}
      />

      {loading && <Loader />}

      {error && (
        <div className="alert alert-danger mt-3 text-center" role="alert">
          {error}
        </div>
      )}

      {response && <ReviewTabs review={response} />}
    </div>
  );
}

export default App;
