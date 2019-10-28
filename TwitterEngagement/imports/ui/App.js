import React, {Component} from 'react';
import {withTracker} from 'meteor/react-meteor-data';
import './App.css';

import {Users} from "../api/users.js";

import Navbar from "./components/layout/Navbar";

class App extends Component {

    render() {
        return (
            <Navbar users={this.props.users} dataReady={this.props.dataReady}/>
        );
    }
}

export default withTracker(() => {
    let ready = Meteor.subscribe("Users").ready();

    return {
        users: Users.find({}).fetch(),
        dataReady: ready
    };
})(App);