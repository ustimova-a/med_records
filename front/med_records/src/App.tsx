import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import DocumentForm from 'components/DocumentForm.tsx';
import DocumentDetails from 'components/DocumentDetails.tsx';

const App: React.FC = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact>
          <DocumentForm onSuccess={() => {}} />
        </Route>
        <Route path="/documents/:id" component={DocumentDetails} />
        {/* Other routes */}
      </Switch>
    </Router>
  );
};

export default App;
