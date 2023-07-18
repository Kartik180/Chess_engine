import React, { useState } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import "./App.css";
import axios from "axios";

const App = () => {
  const [game, setGame] = useState(new Chess());

  const safegameMuatate = (modify) => {
    setGame((g) => {
      const update = new Chess(g.fen());
      modify(update);
      return update;
    });
  };

  const onDrop = (sourceSquare, targetSquare) => {
    try {
      const move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: "q",
      });
      if (move === null) {
        throw new Error("Invalid move!");
      }
      safegameMuatate((game) => game);
      if (game.turn() === 'b') {
        const data = { fen: game.fen(), depth: 3 };
        axios
          .post("http://127.0.0.1:5000/best-move", data, {
            headers: {
              "Content-Type": "application/json",
            },
          })
          .then((response) => response.data)
          .then((data) => {
            safegameMuatate((game) => game.load(data.fen)); // Updated key: data.fen
            if (game.isCheckmate()) {
              alert("Checkmate! Game over.");
              setGame(new Chess());
            } else if (game.isStalemate()) {
              alert("Stalemate! Game over.");
              setGame(new Chess());
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      }
    } catch (error) {
      alert(error.message);
      game.undo();
    }
  };

  return (
    <>
      <div className="main-board">
        <Chessboard position={game.fen()} onPieceDrop={onDrop} />
      </div>
    </>
  );
};

export default App;
