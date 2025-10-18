import { useState } from 'react'
import { withAuthenticator } from '@aws-amplify/ui-react';
import ChapterList from './ChapterList';
import '@aws-amplify/ui-react/styles.css';

function App() {

  return (
    <>
      <ChapterList/>
    </>
  )
}

export default withAuthenticator(App)
