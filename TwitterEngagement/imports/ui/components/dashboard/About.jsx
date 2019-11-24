import React, {Component} from "react";
import Network from "../layout/Network";

class About extends Component {
    constructor(props) {
        super(props);

        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        const parts = name.split(",")
        const type = parts[0]
        const material = parts[1]
        const period = parts[2]

        try {
            const v = parseFloat(value)
            if (v >= 0) {
                Meteor.call("materials.updateCost", type, material, period, value)
            }
        } catch (e) {

        }
    }


    render() {
        return (
            <div className="container-fluid">
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">How to use the app</h4>
                        </div>
                        <div className="card-body ">
                            <p>This web application can help you find the twitter user/s that can obtain the greatest
                                engagement (likes + retweets) when publishing your message. The steps to use the app
                                are:</p>
                            <ol>
                                <li>Go to the search tab</li>
                                <li>Type the message you want to post</li>
                            </ol>
                        </div>
                    </div>
                </div>
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">The Network</h4>
                        </div>
                        <div className="card-body ">
                            <Network/>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default About;