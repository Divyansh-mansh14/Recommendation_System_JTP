import { render, screen } from '@testing-library/react';
import App from './App';

test('renders JTP Recommendations', () => {
  render(<App />);
  const titleElement = screen.getByText(/JTP Recommendations/i);
  expect(titleElement).toBeInTheDocument();
}); 