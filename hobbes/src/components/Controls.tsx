import NavigateNext from "@mui/icons-material/NavigateNext";
import NavigateBeforeIcon from "@mui/icons-material/NavigateBefore";
import TodayIcon from "@mui/icons-material/Today";
import IconButton from "@mui/material/IconButton";

import { h } from "preact";

export function NextButton() {
  const nextComic = async () => {
    await fetch("http://calvinpi.local:8000/api/comics/next", {
      method: "POST",
    });
  };
  return (
    <IconButton onClick={nextComic}>
      <NavigateNext fontSize="large" sx={{ color: "white" }} />
    </IconButton>
  );
}

export function BackButton() {
  const previousComic = async () => {
    await fetch("http://calvinpi.local:8000/api/comics/previous", {
      method: "POST",
    });
  };
  return (
    <IconButton onClick={previousComic}>
      <NavigateBeforeIcon fontSize="large" sx={{ color: "white" }} />
    </IconButton>
  );
}

export function TodayButton() {
  const todaysComic = async () => {
    await fetch("http://calvinpi.local:8000/api/comics/today", {
      method: "POST",
    });
  };
  return (
    <IconButton onClick={todaysComic}>
      <TodayIcon fontSize="large" sx={{ color: "white" }} />
    </IconButton>
  );
}

export function Controls() {
  return (
    <div class="controls">
      <BackButton />
      <TodayButton />
      <NextButton />
    </div>
  );
}
