import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Home } from './Home';
import { About } from './About';
import { NoMatch } from './NoMatch';
import{Layout} from './Components/Layout';
import{NavigationBar} from './Components/NavigationBar'

class App extends Component {
  render() {
    return (
      <React.Fragment>
            <Layout>
              <Router>
                  <Switch>
                    <Route exact path="/" component={Home} />
                    <Route path="/about" component={About} />
                    <Route component={NoMatch} />
                  </Switch>
              </Router>
            </Layout>
      </React.Fragment>
    );
  }
}

export default App;
