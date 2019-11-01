import React from "react";
import PropTypes from 'prop-types';

class SegmentQuestion extends React.Component {

    handleAnswerSubmit(event) {
        console.log(this.state.answer);
        event.preventDefault();
    }

    render() {
        const question_text = this.props.question.text;
        // const question_word_limit = this.props.question.response_word_limit;
        const context_text = this.props.context.text;
        return (
            <div>
                <h4>Context:</h4>
                <div className='segment-context-text'>
                    {context_text}
                </div>
                <h4>Question:</h4>
                <div className='segment-question-text'>
                    {question_text}
                </div>
                <form onSubmit={this.handleAnswerSubmit}>
                    <label><h4>Response:</h4></label>
                    <input
                        type='text'
                        value={this.props.response}
                        onChange={(e) => this.props.onChange(e)}
                    />
                    <input type='submit' value='Submit' />
                </form>

            </div>
        );
    }
}
SegmentQuestion.propTypes = {
    question: PropTypes.object,
    context: PropTypes.object,
    onChange: PropTypes.func,
    response: PropTypes.string,
};

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
            rereading: false,  // we alternate reading and rereading
            document: null,
            segmentQuestionNum: 0,
            segmentContextNum: 0,
            segmentResponseArray: [[]],
        };

        this.handleSegmentResponseChange = this.handleSegmentResponseChange.bind(this);
        this.handleSegmentResponseSubmit = this.handleSegmentResponseSubmit.bind(this);
    }

    async componentDidMount() {
        try {
            // Hardcode the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
        } catch (e) {
            console.log(e);
        }

    }

    prevSegment () {
        // document will be replaced by actual data
        if (this.state.segmentNum > 0){
            this.setState({segmentNum: this.state.segmentNum-1, rereading: true});
        }
    }

    nextSegment () {
        const length = this.state.document.segments.length;
        if (this.state.segmentNum < length){
            if (this.state.rereading) {
                // If we're already rereading, move to the next segment
                this.setState({rereading: false, segmentNum: this.state.segmentNum+1});
            } else {
                // Otherwise, move on to the rereading layout
                this.setState({rereading: true});
            }
        }
    }

    /**
     * Allows the user to change their response to a segment question
     */
    handleSegmentResponseChange(event, question_id) {
        const segmentResponseArray = this.state.segmentResponseArray.slice();

        // If the segment hasn't been added to the responses, initialize it as an array
        if (!segmentResponseArray[this.state.segmentNum]) {
            segmentResponseArray[this.state.segmentNum] = [];
        }

        // The index of the response into the segment is the same as its id
        const segment = segmentResponseArray[this.state.segmentNum];
        segment[question_id] = event.target.value;

        this.setState({segmentResponseArray});
    }

    /**
     * Handles data when a user is trying to submit a response to a question
     */
    handleSegmentResponseSubmit(event) {
        event.preventDefault();


    }


    render() {
        const data = this.state.document;

        if (data) {
            const current_segment = data.segments[this.state.segmentNum];
            const segment_text = current_segment.text;
            const segment_lines = segment_text.split("\r\n");
            const segment_questions = current_segment.questions;
            const segment_contexts = current_segment.contexts;

            // Generate response fields for each of the questions
            const response_fields = segment_questions.map((question_text, id) => {
                return (
                    <SegmentQuestion
                        question={question_text}
                        context={segment_contexts[this.state.segmentContextNum]}
                        onChange={this.handleSegmentResponseChange}
                        response={this.state.segmentResponseArray[this.state.segmentNum][id]}
                        key={id}
                    />
                )
            });

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{data.title}</h1>
                    <div className={"row"}>
                        <div className={"col-8"}>
                            <p>Segment Number: {this.state.segmentNum + 1}</p>
                            {segment_lines.map((line, k) => (
                                <p key={k}>{line}</p>)
                            )}
                            <button
                                className={"btn btn-outline-dark mr-2"}
                                onClick = {() => this.prevSegment()}
                            >
                                Back
                            </button>
                            <button
                                className={"btn btn-outline-dark"}
                                onClick = {() => this.nextSegment()}
                            >
                                {this.state.rereading ? 'Next' : 'Reread'}
                            </button>
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-4"}>
                                {response_fields}
                            </div>
                        }
                    </div>
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }

    }
}

export default ReadingView;
