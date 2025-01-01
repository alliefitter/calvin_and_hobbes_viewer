import { useEffect, useState } from "react";

type Arc = {
  name: string;
  date: string;
};

export function Arcs() {
  const [arcs, setArcs] = useState<Arc[]>([]);
  const [screenWidth, setScreenWidth] = useState<number>(0);
  useEffect(() => {
    const listArcs = async () => {
      const response = await fetch(
        "http://calvinpi.local:8000/api/comics/arcs",
      );
      setArcs(await response.json());
    };
    setScreenWidth(window.innerWidth);
    listArcs();
  }, [setArcs, setScreenWidth]);

  return arcs.length ? (
    <div>
      {arcs.map((arc) => {
        const setArc = async () => {
          await fetch(
            `http://calvinpi.local:8000/api/comics/arcs/${arc.name}`,
            {
              method: "POST",
            },
          );
        };
        const title = arc.name
          .split("_")
          .map((w) => w[0].toUpperCase() + w.substring(1).toLowerCase())
          .join(" ");

        return (
          <a onClick={setArc}>
            <h1>{title}</h1>
            <img
              style={{ width: screenWidth - 200 }}
              src={`http://calvinpi.local:8000/api/comics/image/${arc.date}`}
              loading="lazy"
            />
          </a>
        );
      })}
    </div>
  ) : null;
}
