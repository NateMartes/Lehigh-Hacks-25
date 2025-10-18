import { useState } from 'react'
import { withAuthenticator } from '@aws-amplify/ui-react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChapterList from './ChapterList';
import Chapter from './Chapter';
import QuestionList from './Questions';
import '@aws-amplify/ui-react/styles.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ChapterList />} />
          <Route path="/chapter/:chKey" element={<Chapter />} />
          <Route path="/survey/:chKey" element={<QuestionList />} />
      </Routes>
    </Router>
  );
}

export default withAuthenticator(App);
