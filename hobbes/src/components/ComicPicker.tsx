import { DateCalendar } from "@mui/x-date-pickers/DateCalendar";
import { useEffect, useState } from "react";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs, { Dayjs } from "dayjs";

type ComicCalendarProps = {
  startDate: Dayjs;
  endDate: Dayjs;
  validDates: Dayjs[];
};

function makeDate(date: string): Dayjs {
  const year = date.substring(0, 4);
  const month = date.substring(4, 6);
  const day = date.substring(6, 8);
  return dayjs(`${year}-${month}-${day}`);
}

function ComicCalendar({ startDate, endDate, validDates }: ComicCalendarProps) {
  const [selectedDate, setSelectedDate] = useState<Dayjs>(endDate);
  const disableDate = (date: Dayjs) =>
    !validDates.filter((d) => d.isSame(date));

  const setComic = async (comicDate: Dayjs) => {
    if (selectedDate.year() !== comicDate.year()) {
      setSelectedDate(comicDate);
      return;
    }
    setSelectedDate(comicDate);
    await fetch(
      `http://calvinpi.home:8000/api/comics/${comicDate.format("YYYY-MM-DD")}`,
      { method: "POST" },
    );
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DateCalendar
        onChange={setComic}
        shouldDisableDate={disableDate}
        maxDate={endDate}
        minDate={startDate}
        value={selectedDate}
      />
    </LocalizationProvider>
  );
}

export function ComicPicker() {
  const [startDate, setStartDate] = useState<Dayjs | null>(null);
  const [endDate, setEndDate] = useState<Dayjs | null>(null);
  const [dates, setDates] = useState<Dayjs[]>([]);
  useEffect(() => {
    const listComics = async () => {
      const response = await fetch("http://calvinpi.home:8000/api/comics");
      const rawList: string[] = await response.json();
      setStartDate(makeDate(rawList[0]));
      setEndDate(makeDate(rawList[rawList.length - 1]));
      for (const date of rawList) {
        dates.push(makeDate(date));
      }
      setDates(dates);
    };
    listComics();
  }, [setDates, dates, setStartDate, setEndDate]);

  return dates.length ? (
    <div>
      <h1>Select a date.</h1>
      <ComicCalendar
        startDate={startDate}
        endDate={endDate}
        validDates={dates}
      />
    </div>
  ) : null;
}
