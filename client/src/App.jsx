import { useState } from 'react'
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

function App() {

  return (
    <>
      <div className="flex text-x1 text-blue-800">
        <p>Hello World!</p>
        <p>Hello HenHacks</p>
      </div>
    </>
  )
}

export default withAuthenticator(App)
