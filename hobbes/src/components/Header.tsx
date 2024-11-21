import { useLocation } from "preact-iso";
import { Controls } from "./Controls";

export function Header() {
  const { url } = useLocation();

  return (
    <header>
      <Controls />
      <nav>
        <a href="/" class={url == "/" && "active"}>
          Home
        </a>
        <a href="/arcs" class={url == "/arcs" && "active"}>
          Arcs
        </a>
      </nav>
    </header>
  );
}
