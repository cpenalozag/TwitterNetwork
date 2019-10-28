import React, {Component} from "react";

class Dashboard extends Component {

    constructor(props) {
        super(props);
        this.max_chars = 280;
        this.state = {
            chars_left: this.max_chars
        };
        this.handleSearch = this.handleSearch.bind(this);
    }

    handleChange(event) {
        let input = event.target.value;
        this.setState({
            chars_left: this.max_chars - input.length
        });
    }

    handleSearch() {

    }

    render() {
        return (
            <div className="container-fluid">
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">Search users for your campaign</h4>
                            <p>Insert the text you want to post to Twitter. The search will find the best users to post it!</p>
                        </div>
                        <hr/>
                        <div className="card-body ">
                            <p>Tweet message:</p>
                            <textarea onChange={this.handleChange.bind(this)} name="tweet-text" cols="40" className="text-input" rows="4"></textarea>
                            <p className={`chars-left ${this.state.chars_left<0?"red":""}`}>Characters Left: {this.state.chars_left}</p>
                        </div>
                        <div className="row">
                            <div className="col-md-2 mx-auto">
                                <input className={`btn btn-primary`} type="submit" value="Search" onClick={this.handleSearch} />
                            </div>
                        </div>
                    </div>
                </div>
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">Results</h4>
                        </div>
                        <div className="card-body ">
                            <p>List</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Dashboard;