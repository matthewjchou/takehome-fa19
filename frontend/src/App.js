import React, { Component } from 'react'
import Instructions from './Instructions'
import Contact from './Contact'
import Counter from './Counter'

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      contacts: [
        {id: 1, name: "Angad", nickname: "greg", hobby: "dirty-ing"},
        {id: 2, name: "Roy", nickname: "uwu", hobby: "weeb"},
        {id: 3, name: "Daniel", nickname: "oppa", hobby: "losing money with options trading"},
      ],
      name: "",
      nickname: "",
      hobby: ""
    }

    this._child = React.createRef();
  }

  handleChangeName = (event) => {
    this.setState({name: event.target.value})
  }

  handleChangeNickname = (event) => {
    this.setState({nickname: event.target.value})
  }

  handleChangeHobby = (event) => {
    this.setState({hobby: event.target.value})
  }

  resetFormState() {
    this.setState({name: "", nickname: "", hobby: ""})
  }

  handleSubmit = () => {
    this.setState(prevState => {
      var newContacts = JSON.parse(JSON.stringify(prevState.contacts))
      newContacts.push({id: prevState.contacts.length + 1, name: this.state.name,
        nickname: this.state.nickname, hobby: this.state.hobby})
      
      return {contacts: newContacts}
    })
    this.increaseCounter()
    this.resetFormState()
    this._child.current.handleIncrement()

  }

  increaseCounter = () => {
    this.setState({increaseCount: true})
  }

  render() {
    return ( 
      <div className="App">
        <Instructions complete={true} />
        <Counter ref={this._child} />
        {this.state.contacts.map(x => (
          <Contact id={x.id} name={x.name} nickname={x.nickname} hobby={x.hobby} />
        ))}

        <form>
          <label onSubmit={this.handleSubmit}>
            Name:
            <input type="text" value={this.state.name} onChange={this.handleChangeName} />
            <br></br>
            Nickname:
            <input type="text" value={this.state.nickname} onChange={this.handleChangeNickname} />
            <br></br>
            Hobby:
            <input type="text" value={this.state.hobby} onChange={this.handleChangeHobby} />
          </label>
          <p>
            <input type="button" value="Create Contact" onClick={this.handleSubmit} />
          </p>
        </form>
      </div>
    )
  }
}

export default App
