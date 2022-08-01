import React from "react";
import AgendaItem from "./AgendaItem.jsx"
import DOMPurify from 'dompurify';
import Parser from 'html-react-parser';
import BackendMethods from "./BackendMethods.jsx";

export default class Agenda extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      errors: false
    };

    this.ITEM = "Meeting/" + this.props.match.params.meetingId + "/Agenda/"
  }

  async componentDidMount() {
    const data = await BackendMethods.fetchItems(this.ITEM)
    if (!data) {
      this.setState({errors:true});
    }
    this.setState({ data: data[0]});

    const meetingData = await BackendMethods.fetchItems("Meeting/" + this.props.match.params.meetingId + "/");
    if (!meetingData) {
      this.setState({errors:true});
    }
    this.setState({ meetingData: meetingData, loading: false });
  }

  render() {
    if (this.state.errors) {
      return <div>could not retrieve agenda information</div>
    }

    if (this.state.loading) {
      return <div></div>;
    }

    if (!this.state.data) {
      return <div>didn't get an agenda</div>;
    }

    return <div>
        <div className="agenda-title">
          <div className="flex"><img src={require('./../img/tpsb_icon.png').default} alt="Toronto Police Services Board Icon"/></div>
          <br></br>
          <h1 style={{ textAlign: "Center" }}>Online Virtual Meeting</h1>
          <h1 style={{ textAlign: "Center" }}>{this.state.meetingData.date.substring(0, this.state.meetingData.date.indexOf('T')).split('/').reverse()}</h1>
          <h1 style={{ textAlign: "Center" }}>At {this.state.meetingData.date.substring(this.state.meetingData.date.indexOf('T') + 1, this.state.meetingData.date.length).split('-')[0]}</h1>
          <br></br>
          <div className="meetingDescription" style={{ textAlign: "Center" }}> {Parser(DOMPurify.sanitize(this.state.meetingData.description))}</div>
          <h2 style={{ textAlign: "Center" }}>Agenda Items For Consideration:</h2>
        </div>
        <div>

          <AgendaItem agenda={this.state.data}/>
        </div>
        <br></br>
      </div>;
  }
}
