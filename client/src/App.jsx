import { Authenticator } from '@aws-amplify/ui-react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChapterList from './Homepage';
import Chapter from './Chapter';
import LoginHeader  from './LoginHeader';
import QuestionList from './Questions';
import '@aws-amplify/ui-react/styles.css';
import './amplify.css';


function App() {

  const components = {
    Header: LoginHeader
  };

  return (
    <Router>
      <Authenticator components={components} className="flex h-svh justify-center">
          <Routes>
            <Route path="/" element={<ChapterList />} />
              <Route path="/chapter/:chKey" element={<Chapter />} />
              <Route path="/survey/:chKey" element={<QuestionList />} />
          </Routes>
      </Authenticator>
    </Router>
  );
}

export default App;
