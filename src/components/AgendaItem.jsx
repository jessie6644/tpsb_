import React, { Fragment } from "react";
import DOMPurify from 'dompurify';
import Parser from 'html-react-parser';
import BackendMethods from "./BackendMethods";
import {CSSTransition} from 'react-transition-group';

export default class AgendaItem extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      errors: false
    };

    this.ITEM = "Meeting/" + this.props.agenda.meeting + "/Agenda/" + this.props.agenda.id + "/AgendaItem/"
  }

  async componentDidMount() {
    const data = await BackendMethods.fetchItems(this.ITEM)
    if (!data) {
      this.setState({errors:true});
    }
    this.setState({ data: data, loading: false });
  }

  setCurrentAgendaItem(agendaItem) {
    if (this.state.currentAgendaItem === agendaItem) {
      this.setState({currentAgendaItem: "blah"})
    } else {
        this.setState({currentAgendaItem: agendaItem});
    }
  }

  setCurrentAgendaItemKeyPress(e, agendaItem) {
    if (e.key === 'Enter') {
      this.setCurrentAgendaItem(agendaItem);
    }
  }

  displayResult(result) {
    const POSSIBLE_DECISIONS = {'TBC': 'To be considered', 'CUC': 'Currently under consideration', 'A': 'Approved',
                            'AWM': 'Approved with motion', 'R': 'Rejected'};
    return POSSIBLE_DECISIONS[result].toUpperCase();
  }

  displayAgendaItemDetails(item) {
    return <div>
      <img width="50%" src={require('./../img/tpsb_dropdown_header.png').default} alt="Toronto Police Services Board black and white icon header"/>
      <div>
        <div style={{ textAlign: "Left" }}> {Parser(DOMPurify.sanitize(item.description))}</div>
        {item.result && <div style={{fontWeight: 'bold'}}>STATUS: {this.displayResult(item.result)}</div>}
        <div>{Parser(DOMPurify.sanitize(item.motion))}</div>
        {item.file && <a className="download-attach" href={item.file} download>Download Attachments: {item.file ? item.file.split('/').pop() : item.file}</a>}
        <br></br>
      </div>
    </div>
  }

  render() {
    if (this.state.errors) {
      return <div>could not retrieve agenda information</div>
    }

    if (this.state.loading) {
      return <div></div>;
    }

    if (!this.state.data) {
      return <div>didn't get an agenda item</div>;
    }

    return <table className="agendaItem-table">
      <tbody>
        <tr>
          <th>Number</th>
          <th>Title</th>
        </tr>
        {this.state.data.sort((a,b) => a.number - b.number).map((agendaItem) => {
          return <Fragment>
            <tr key={agendaItem.id} onClick={() => this.setCurrentAgendaItem(agendaItem)} tabIndex="0" onKeyDown={(e) => this.setCurrentAgendaItemKeyPress(e, agendaItem)}>
              <td>{agendaItem.number}</td>
              <td>{agendaItem.title}</td>
            </tr>
            <tr className="trh">
              <td height="auto" colspan="2" padding="0">
                <CSSTransition in={this.state.currentAgendaItem && this.state.currentAgendaItem === agendaItem}
                                timeout={1000}
                                classNames="dropdown"
                                unmountOnExit>
                  <div height="auto" position="relative">
                    {this.state.currentAgendaItem && this.displayAgendaItemDetails(agendaItem)}
                  </div>
                </CSSTransition>
              </td>
            </tr>
          </Fragment>
        })}
      </tbody>
    </table>

  }
}
