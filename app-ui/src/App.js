import React from 'react';
import './App.css';
import { Layout } from 'antd';
import GetInfo from './components/GetInfo';
import logo from "./images/coronavirus-abc.png"
const { Header, Footer, Content } = Layout;

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <Layout>
        <Header>
          <img width="50%" className="example-link-icon" src={logo} alt="website logo"></img>
        </Header>
          <Content>
            <GetInfo></GetInfo>
          </Content>
        <Footer>
          * All information is provided by Johns Hopkins University CCSE. *
        </Footer>
      </Layout>
        
      </header>
    </div>
  );
}

export default App;
