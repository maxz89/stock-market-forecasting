import React, { useState } from 'react';
import {
  Container,
  TextField,
  Button,
  Paper,
  Typography,
  Radio,
  RadioGroup,
  FormControlLabel,
  LinearProgress,
} from '@mui/material';

const TickerPrompt = () => {
  const [ticker, setTicker] = useState('');
  const [forecast, setForecast] = useState('');
  const [low, setLow] = useState('');
  const [high, setHigh] = useState('');
  const [model, setModel] = useState('');
  const [isLoadbar, setIsLoadbar] = useState(false);

  const handleQuestionSubmit = async () => {
    // Simulate a response from a chatbot (replace with actual API call)
    setIsLoadbar(true);
    setForecast('');
    const response: string = await getForecast(ticker);
    setIsLoadbar(false);

    // Set the response in the state
    setForecast(response);
  };

  const getForecast = async (ticker: string) => {
    // In a real application, you would send the question to a chatbot API
    // and receive a response. For simplicity, we're just echoing the question.
    const res = await fetch("http://localhost:80/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "model": model,
        "ticker": ticker
      })
    });
    const body = await res.json();
    setLow(body.low);
    setHigh(body.high);
    return body.forecast;
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} style={{ padding: '20px', marginTop: '20px' }}>
        <Typography variant="h5">Stock Price Forecaster</Typography>
        <TextField
          fullWidth
          label="Enter a Ticker"
          variant="outlined"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          margin="normal"
        />
        <RadioGroup
          value={model}
          onChange={(e) => setModel(e.target.value)}
        >
          <FormControlLabel
            value="ARIMA"
            control={<Radio />}
            label="ARIMA"
          />
          <FormControlLabel
            value="ETS"
            control={<Radio />}
            label="ETS"
          />
          <FormControlLabel
            value="Theta"
            control={<Radio />}
            label="Theta"
          />
        </RadioGroup>
        <Button
          variant="contained"
          color="primary"
          onClick={handleQuestionSubmit}
        >
          Submit
        </Button>
        {isLoadbar && (
          <div style={{ marginTop: '20px' }}>
            <LinearProgress />
            <Typography variant="subtitle1">fetching data and training model...</Typography>
          </div>
        )}
        {forecast && (
          <div style={{ marginTop: '20px' }}>
            <Typography variant="h6">Next Day Forecasted Price:</Typography>
            <Typography>{forecast}</Typography>
            <Typography variant="h6">90% Confidence Interval:</Typography>
            <Typography>{"["}{low}{" - "}{high}{"]"}</Typography>
          </div>
        )}
      </Paper>
    </Container>
  );
};

export default TickerPrompt;
