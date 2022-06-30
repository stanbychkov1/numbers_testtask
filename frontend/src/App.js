import './App.css';
import {useEffect, useState} from "react";
import axios from "axios";

function isDifferentDates(d2) {
    let today = new Date()
    let day = new Date(d2)
  return day < today;
}

const Orders = () => {
  const [orders, setOrders] = useState([]);
useEffect(() => {
  fetchOrders();
}, []);
const fetchOrders = () => {
    axios
    .get('http://127.0.0.1/api/orders/')
    .then((res) => {
      console.log(res);
      setOrders(res.data);
    })
    .catch((err) => {
      console.log(err);
    });
};
return (
    <table>
      <thead>
        <tr>
          <th>№</th>
          <th>Номер заказа</th>
          <th>Стоимость в USD</th>
          <th>Стоимость в руб.</th>
          <th>Дата доставки</th>
        </tr>
      </thead>
      <tbody>
        {
          orders.map((order, index) => {
            return (
              <tr key={index} bgcolor={isDifferentDates(order.shipment_date) ? 'red' : ''}>
                <td>{index+1}</td>
                <td>{order.order_number}</td>
                <td>{order.usd_price}</td>
                <td>{order.rub_price}</td>
                <td>{order.shipment_date}</td>
               </tr>
            );
          })
        }
        </tbody>
    </table>
  );
};




function App() {
  return (
    <div className='App'>
      <Orders />
    </div>
  )
}

export default App;
