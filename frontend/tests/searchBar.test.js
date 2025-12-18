// Simple test for the SearchBar component
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SearchBar from '../src/components/SearchBar';

describe('SearchBar Component', () => {
  test('renders search input and button', () => {
    render(<SearchBar />);
    
    const inputElement = screen.getByPlaceholderText('Search textbook...');
    const buttonElement = screen.getByLabelText('Search');
    
    expect(inputElement).toBeInTheDocument();
    expect(buttonElement).toBeInTheDocument();
  });
  
  test('updates input value on change', () => {
    render(<SearchBar />);
    
    const inputElement = screen.getByPlaceholderText('Search textbook...');
    
    fireEvent.change(inputElement, { target: { value: 'test query' } });
    
    expect(inputElement.value).toBe('test query');
  });
  
  test('calls onSearch callback when search is triggered', () => {
    const mockOnSearch = jest.fn();
    render(<SearchBar onSearch={mockOnSearch} />);
    
    const inputElement = screen.getByPlaceholderText('Search textbook...');
    fireEvent.change(inputElement, { target: { value: 'test' } });
    
    const buttonElement = screen.getByLabelText('Search');
    fireEvent.click(buttonElement);
    
    expect(mockOnSearch).toHaveBeenCalledWith('test');
  });
});