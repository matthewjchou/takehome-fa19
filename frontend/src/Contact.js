import React, { Component } from 'react'

class App extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props)
  }
  render() {
    const {id, name, nickname, hobby} = this.props
    return (
      <div className="Contact">
        <h4>{name}</h4>
      </div> 

    )
  } 
}

export default App
