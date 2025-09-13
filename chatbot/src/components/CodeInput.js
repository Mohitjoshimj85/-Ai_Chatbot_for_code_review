import React from 'react';

function CodeInput({ code, setCode, language, setLanguage, onSubmit }) {
  return (
    <div className="mb-4">
      <div className="mb-3">
        <label className="form-label">Select Language</label>
        <select className="form-select" value={language} onChange={e => setLanguage(e.target.value)}>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
        </select>
      </div>

      <div className="mb-3">
        <label className="form-label">Enter Code</label>
        <textarea
          className="form-control"
          rows="10"
          value={code}
          onChange={e => setCode(e.target.value)}
          placeholder="Write your code here..."
        ></textarea>
      </div>

      <button className="btn btn-primary" onClick={onSubmit}>Submit</button>
    </div>
  );
}

export default CodeInput;
