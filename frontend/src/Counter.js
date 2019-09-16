import React, { Component } from 'react'

class Counter extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props)
    this.state = {count:0}

  }

  handleIncrement = () => {
    this.setState(prevState => {
      return {count: prevState.count + 1}
    })
  } 

  handleDecrement = () => {
    this.setState(prevState => {
      return {count: prevState.count - 1}
    })
  } 
  render() {
    const {count} = this.state  
    
    return (
      <div className="Counter">
        <p>
          The current count is: {count}  
        </p>
        <button onClick={this.handleIncrement}>Increment</button>
        <button onClick={this.handleDecrement}>Decrement</button>
      </div>
    )
  }
}

export default Counter
