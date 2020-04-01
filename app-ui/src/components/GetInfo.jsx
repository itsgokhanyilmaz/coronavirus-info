import React, { Component } from 'react';
import { Layout, Input } from 'antd';
import CovidChart from './CovidChart';
import coronainfo from "../api/coronainfo";

import 'antd/es/input/style/index.css';
import 'antd/es/select/style/index.css';

const { Header } = Layout;
const { Search } = Input;

class GetInfo extends Component{
    constructor(props){
        super(props)

        this.state ={
            country: "Unknown",
            results: [],
        };
    }

    getSearchResult = async (country) => {
        const response = await coronainfo.get(`/get_corona?country=${country}`) 

        this.setState({
            results: response.data,
            country: country
        });
        console.log(response.data)
    }

    render(){

        const covidData = [
            { name: 'Active', value: this.state.results["Active"] },
            { name: 'Death', value: this.state.results["Deaths"] },
            { name: 'Recovered', value: this.state.results["Recovered"] },
            { name: 'Confirmed', value: this.state.results["Confirmed"] },
        ];
        
        return(
            <div>
                <Header>
                    <Search
                        size="large"
                        style={{width:500}}
                        placeholder="Type a country"
                        onSearch={value => this.getSearchResult(value)}
                    />
                    <br></br>
                    Country: {this.state.country } - Total Case: {this.state.results["Confirmed"]}
                    <CovidChart info={covidData}></CovidChart>
                </Header>
            </div>
        )
    }
}

export default GetInfo;