import React from 'react';
import { LineChart, XAxis, YAxis, Tooltip, CartesianGrid, Line } from 'recharts';


class TableDisplay extends React.Component {
  constructor() {
    super();
    this.state = {
      Data: null
    };
  }
  componentDidMount() {
    let hostname = window.location.hostname;
    hostname = hostname.substring(0, hostname.length - 5);
    const URL = "http://" + window.location.hostname + ":1000/orders";
    fetch(URL).then(res => res.json()).then(json => {
      this.setState({ Data: json });
    });
  }
  render() {
    const Data = this.state.Data;
    if (!Data) return <div>Loading</div>;
    return (
      <div className="Table">
      <table>
      <tr><th>№</th><th>Номер заказа</th><th>Стоимость, $</th><th>Стоимость, ₽</th><th>Срок поставки</th></tr>
      {Data.orders.map((order, index) => (
        <tr>
          <td>{order.google_id}</td>
          <td>{order.number}</td>
          <td>{order.price_usd}</td>
          <td>{order.price_rub}</td>
          <td>{order.date}</td>
        </tr>
      ))}
      </table>
    </div>
    );
  }
}


class TableTotalDisplay extends React.Component {
  constructor() {
    super();
    this.state = {
      Data: null
    };
  }
  componentDidMount() {
    let hostname = window.location.hostname;
    hostname = hostname.substring(0, hostname.length - 5);
    const URL = "http://" + window.location.hostname + ":1000/orders";
    fetch(URL).then(res => res.json()).then(json => {
      this.setState({ Data: json });
    });
  }
  render() {
    const Data = this.state.Data;
    if (!Data) return <div>Loading</div>;
    return (
      <div className="TableTotal">
      <table class="tt-table">
      <tr class="tt-table"><th class="tt-table">Total</th></tr>
      <tr class="tt-table">
          <td class="tt-table">{Data.total}</td>
      </tr>
      </table>
    </div>
    );
  }
}


class App extends React.Component {
  constructor() {
    super();
    this.state = {
      Data: null
    };
  }
  componentDidMount() {
    let hostname = window.location.hostname;
    hostname = hostname.substring(0, hostname.length - 5);
    const URL = "http://" + window.location.hostname + ":1000/orders_sum";
    fetch(URL).then(res => res.json()).then(json => {
      this.setState({ Data: json });
    });
  }
  render() {
    const Data = this.state.Data;
    if (!Data) return <div>Loading</div>;
    return (
      <div className="App">
        <table class="d-table">
          <tr class="d-table">
            <td class="d-table">
            <LineChart
              width={800}
              height={400}
              data={Data}
              margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            >
              <XAxis dataKey="date" />
              <YAxis dataKey="price_usd" displayName="Стоимость, $" />
              <Tooltip />
              <CartesianGrid stroke="#f5f5f5" />
              <Line type="monotone" dataKey="price_usd" stroke="#ff7300" yAxisId={0} />
            </LineChart>
            </td>
            <td class="d-table">
              <TableTotalDisplay/>
              <TableDisplay/>
            </td>
          </tr>
        </table>
      </div>
    );
    }
}

export default App;
