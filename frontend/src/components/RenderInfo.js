import React from 'react';

export function RenderInfo(props) {
    const { distance_by_foot, distance_by_direction, distance_by_shortest, distance_by_super,counter_super_best, program_runs } = props.results;

    return (
        <div>
        <div className="info">
            <ul>
            <li>The route begins at the <span className="yellow">logistics office</span> and gradually turns <span className="green">green.
            </span> A <span className="red">(number)</span> marks a delivery drop-off.</li>
            <li>If an address is visited twice, it retains the color gradient from the first visit.</li>
            <li>Connection between adjacent tiles is not always possible. Click on an address to view its info.</li>
            <li>The distances for 4 different delivery methods have been calculated in the table below. All routes end at the office, and all routes use the A* search algorithm to find the shortest route to the next drop-off. 
                The difference between them is their sorting. The 'Super Deliveries' method tries to beat the method that sorts drop offs after compass direction.</li>
            </ul>
           
        <table className="info">
            <thead>
                <tr>
                    <th>Delivery method</th>
                    <th>Route distance</th>
                    <th>Distance saved</th>
                </tr>
            </thead>
        <tbody>    
        <tr>
            <td>1-by-1, returning to the office for every delivery</td>
            <td>{distance_by_foot} km</td>
            <td>-</td>
        </tr>
        <tr>
            <td>Sorted after shortest distance from office</td>
            <td>{distance_by_shortest} km</td>
            <td>{distance_by_foot - distance_by_shortest} km</td>
        </tr>
        <tr>
            <td>Sorted by direction</td>
            <td>{distance_by_direction} km</td>
            <td>{distance_by_foot - distance_by_direction} km</td>
        </tr>
        <tr>
        <td>Optimized by Super Deliveries (route shown above)</td>
        <td>{distance_by_super} km</td>
        <td>{(distance_by_super <= distance_by_direction) ? <span className="super">{distance_by_foot - distance_by_super}</span>: <span>{distance_by_foot - distance_by_super}</span>} km</td>
        </tr>
        </tbody>
        </table>
        </div>
        <div className="info">
        <p className="info">'Super Deliveries' has found the fastest route {counter_super_best} times out of {program_runs} delivery runs. Reload orders to randomize new delivery addresses and run again!</p>
        </div>
        </div>
    );
}