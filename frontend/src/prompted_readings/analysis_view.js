import React from "react";

class AnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // we initialize analysis to null, so we can check in render() whether
            // we've received a response from the server yet
            analysis: null,
        }
    }

    /**
     * This function is fired once this component has loaded into the DOM.
     * We send a request to the backend for the analysis data.
     */
    async componentDidMount() {
        try {
            const response = await fetch('/api/analysis/');
            const analysis = await response.json();
            this.setState({analysis});
        } catch (e) {
            // For now, just log errors to the console.
            console.log(e);
        }
    }
    //
    /**
     * Create paragraph tags for the question and revisit count
     */
    // let revisits = median_revisits.map((medians) =>
    //     <p>{medians}</p>
    // );

    render() {
        if (this.state.analysis !== null) {
            const {  // object destructuring:
                total_view_time,
                median_revisits,
            } = this.state.analysis;
            return (
                <div>
                    <h1>Analysis of Student Responses</h1>
                    <h3>Total view time</h3>
                    <p>{total_view_time} seconds</p>
                    <h3>Median times a question was revisited</h3>
                    { Object.keys(median_revisits).map(function(median, i){
                        return <p key={i}> {median} : {median_revisits[median]} </p>;
                    })}
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }
}

export default AnalysisView;
