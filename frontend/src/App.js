
import axios from 'axios'
import React from 'react'

import '../node_modules/bootstrap/dist/css/bootstrap.min.css'; 
import BootstrapTable from 'react-bootstrap-table-next';

class App extends React.Component {
    state = { total: 0, orders: []} 
    
    
    componentDidMount() {
        let data;
        axios.get('http://127.0.0.1:8000')
        .then(res => {
            data = res.data;
            this.setState({
                total: data.total,
                orders: data.orders,
            });
        })
        .catch(err => {
            console.log(err)
        })
    }

    columns = [{
      dataField: 'n',
      text: '№'
    },{
      dataField: 'number',
      text: 'Заказ №'
    }, {
      dataField: 'price_usd',
      text: 'Стоимость,$'
    }, {
      dataField: 'date',
      text: 'скрок поставки'
    }];


    graph_data = {
      labels: ["Sunday", "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday", "Saturday"],
      datasets: [
        {
          label: "Hours Studied in Geeksforgeeks",
          data: [2, 5, 7, 9, 7, 6, 4],
          fill: true,
          backgroundColor: "rgba(6, 156,51, .3)",
          borderColor: "#02b844",
        }
      ]
    }

    render() {
      return (
      
      <div>
        <div>
          <h1>Total</h1>
          <h1>{this.state.total}</h1>
        </div>
        <div style={{width: "50%"}}>
          <BootstrapTable keyField='n' data={this.state.orders} columns={this.columns} />
        </div>
      </div>
      
      )
    }
}

export default App;
