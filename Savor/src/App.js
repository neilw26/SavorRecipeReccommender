import React from 'react';
import { Routes, Route } from 'react-router-dom';
import RecipeFinder from './RecipeFinder';

const App = () => {
  return (
    <div>
      <div className="content">
        <Routes>
          <Route path="/" element={<RecipeFinder />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
