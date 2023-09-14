
import "./draggablebox.css";
import React, { useState, useRef } from "react";
import Draggable from "react-draggable";


const Piece = () => {
  const [currentPosition, setCurrentPosition] = useState({ xRate: 150, yRate: 150 });
  const draggableRef = useRef(null);

  const onDrag = (e, data) => {
    setCurrentPosition({ xRate: data.x, yRate: data.y });
  };

  return (
    <div>
      <Draggable
        position={{
          x: currentPosition.xRate,
          y: currentPosition.yRate
        }}
        onDrag={onDrag}
        nodeRef={draggableRef}
      >
        <div className="Piece" ref={draggableRef}>
          <span className="Piece-phrase"></span>
        </div>
      </Draggable>
    </div>
  );
};

export default Piece;
