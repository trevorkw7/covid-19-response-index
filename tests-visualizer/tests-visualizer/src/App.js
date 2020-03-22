import React, { useState } from 'react';
import ReactMapGL, { Marker } from "react-map-gl";
import * as testData from "./data/our_world_parsed.json"



export default function App(){
  const[viewport, setViewport] = useState({
    latitude: 25,
    longitude: 5,
    width: "100vw",
    height: "100vh",
    zoom: 2
  });

return (
<div>
  <ReactMapGL
    {...viewport}
    mapboxApiAccessToken={"pk.eyJ1IjoidHJldm9ya3c3IiwiYSI6ImNrODJsZnA3ZjBua3czZXFxNTQ4NTM3NmcifQ.OKs665Uu8Na_Znmlr4V-zg"}
    onViewportChange={viewport => {
      setViewport(viewport);
    }}
    >
      {testData.map()}
  </ReactMapGL>
</div>
);
}
