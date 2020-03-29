import React, { Component } from 'react';

import { Layout, Input } from 'antd';
import axios from 'axios';
import CovidChart from './CovidChart';
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

    getSearchResult(country){
        axios({
            method : 'get',
            url: `http://127.0.0.1:5000/get_corona?country=${country}`
        }).then(obj => {
            this.setState({
                results: obj.data,
                country: country
            });
            console.log(obj.data)
        })
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