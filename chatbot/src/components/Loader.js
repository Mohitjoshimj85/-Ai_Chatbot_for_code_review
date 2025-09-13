import React from 'react';

function Loader() {
  return (
    <div className="text-center my-4">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p>Generating review...</p>
    </div>
  );
}

export default Loader;
